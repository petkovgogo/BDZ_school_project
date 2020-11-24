from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormView

from .models import Station, Ticket
from .forms import LoginForm, RegisterForm, BuyTicketForm


class LoginView(FormView):
    template_name = 'client/login.html'
    form_class = LoginForm
    success_url = '/auth/'


class RegisterView(FormView):
    template_name = 'client/register.html'
    form_class = RegisterForm
    success_url = '/signup/'


class BuyTicket(FormView):
    template_name = 'client/product.html'
    form_class = BuyTicketForm
    success_url = '/buy/'


def index(request):
    return render(request, 'client/index.html')


def authenticate_user(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('client:index'))
        else:
            form.add_error('username', 'Invalid credentials')
            form.add_error('password', 'Invalid credentials')
    return render(request, 'client/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.clean_username()
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('client:index'))
    return render(request, 'client/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'client/index.html')

def buy_ticket(request):
    form = BuyTicketForm(request.POST)
    if form.is_valid():
        return HttpResponseRedirect(reverse('client:index'))
    return render(request, 'client/product.html', {'form': form})
