from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    email = forms.EmailField(label='Enter your email', max_length=100)
    password = forms.CharField(label='Enter your password', max_length=100, min_length=8)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Enter your first name', max_length=100, required=False)
    last_name = forms.CharField(label='Enter your last name', max_length=100, required=False)
    username = forms.CharField(label='Enter your username', max_length=100)
    email = forms.EmailField(label='Enter your email', max_length=100)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
