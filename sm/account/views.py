from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, VerifyRegisterForm
import random
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib import messages


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












