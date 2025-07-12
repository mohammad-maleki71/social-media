from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, VerifyRegisterForm, UserLoginForm, UserProfileUpdateForm
import random
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from home.models import Relation


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'account/register.html'
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            request.session['user_register_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password2'],
            }
            messages.success(request, 'your code sent successfully', 'success')
            return redirect('account:verify_register')
        return render(request, self.template_name, {'form': form})


class UserVerifyRegisterView(View):
    form_class = VerifyRegisterForm
    template_name = 'account/verify_register.html'
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        user_session = request.session['user_register_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if code_instance.code == cd['code']:
                User.objects.create_user(user_session['phone_number'],
                                         user_session['email'],
                                         user_session['full_name'],
                                         user_session['password']
                                         )
                code_instance.delete()
                messages.success(request, 'your registered successfully', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'your code is invalid', 'danger')
                return redirect('account:verify_register')
        return render(request, self.template_name, {'form': form})

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'your login successfully', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            else:
                messages.error(request, 'your login is invalid', 'danger')
            return redirect('account:login')
        return render(request, self.template_name, {'form': form})

class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'your logout successfully', 'success')
        return redirect('home:home')

class UserProfileView(LoginRequiredMixin,View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        posts = user.posts.all()
        is_following = False
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation:
            is_following = True
        return render(request, 'account/profile.html', {'user':user, 'posts':posts, 'is_following':is_following})

class UserProfileUpdateView(LoginRequiredMixin,View):
    form_class = UserProfileUpdateForm
    template_name = 'account/profile_update.html'

    def get(self, request, user_id):
        form = UserProfileUpdateForm(instance=request.user.profile, initial={'email': request.user.email,
                                                                             'full_name': request.user.full_name,
                                                                             'phone_number': request.user.phone_number
                                                                             })
        return render(request, self.template_name, {'form':form})

    def post(self, request, user_id):
        form = UserProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.full_name = form.cleaned_data['full_name']
            request.user.phone_number = form.cleaned_data['phone_number']
            request.user.save()
            messages.success(request, 'your profile updated successfully', 'success')
            return redirect('account:profile', request.user.id)
        return render(request, self.template_name, {'form':form})


class UserPasswordResetView(auth_view.PasswordResetView):
    template_name = 'account/password_reset.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'

class UserPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'

class UserPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')

class UserPasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'















