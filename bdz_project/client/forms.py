from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(label='Enter your username', max_length=100)
    password = forms.CharField(label='Enter your password',
                               max_length=100, min_length=8, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        label='Enter your first name', max_length=100, required=False)
    last_name = forms.CharField(
        label='Enter your last name', max_length=100, required=False)
    username = forms.CharField(label='Enter your username', max_length=100)
    email = forms.EmailField(label='Enter your email', max_length=100)
    password = forms.CharField(label='Enter your password',
                               max_length=100, min_length=8, widget=forms.PasswordInput)
    conf_password = forms.CharField(label='Confirm your password',
                                    max_length=100, min_length=8, widget=forms.PasswordInput)
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('conf_password')

        if password1 != password2:
            raise forms.ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password']
        )
        return user
