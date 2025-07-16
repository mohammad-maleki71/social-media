from django import forms
from .models import User, Profile
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


class UserCreateForm(forms.ModelForm):

    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['phone_number', 'email', 'full_name']


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(help_text="you can change Password using <a href=\"../password/\">this form</a>.")

    class Meta:
        model = User
        fields = ['phone_number', 'email', 'full_name','password','last_login']


class UserRegisterForm(forms.Form):
    phone_number = forms.CharField(label='phone number', widget=forms.TextInput)
    email = forms.EmailField()
    full_name = forms.CharField(label='full name', widget=forms.TextInput)
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError('Passwords don\'t match')

class VerifyRegisterForm(forms.Form):
    code = forms.IntegerField()

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(
        label="شماره تلفن",
        max_length=11,
        widget=forms.TextInput(attrs={
            'type': 'tel',
            'autocomplete': 'tel',
            'inputmode': 'numeric',
            'pattern': '[0-9]{11}',
            'placeholder': 'مثلاً 09123456789'
        })
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password'
        })
    )


class UserProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    full_name = forms.CharField()
    phone_number = forms.CharField()

    class Meta:
        model = Profile
        fields = ('age', 'bio')




