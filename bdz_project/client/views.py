from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic.edit import FormView

from .models import Station, Ticket
from .forms import LoginForm, RegisterForm


class LoginView(FormView):
    template_name = 'client/login.html'
    form_class = LoginForm
    success_url = '/auth/'


class RegisterView(FormView):
    template_name = 'client/register.html'
    form_class = RegisterForm
    success_url = '/signup/'

class BuyTicket(generic.ListView):
    model = Station
    template_name = 'client/product.html'

def index(request):
    return render(request, 'client/index.html', {})

def authenticate_user(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        user = authenticate(username='john', password='secret')
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('client:index'))
    else:
        form = LoginForm()
    return render(request, 'client/login.html')

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('client:index'))
    else:
        form = RegisterForm()
    return render(request, 'client/register.html', {'form': form})

def buy_ticket(request):
    return HttpResponseRedirect(reverse('client:index'))
