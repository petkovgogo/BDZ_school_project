from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login

def login_user(request):
    return render(request, 'client/login.html', {})

def authenticate_user(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('client:index'))
    else:
        context = {
            'message': True,
        }
        return HttpResponseRedirect(reverse('client:login', context))

def index(request):
    return render(request, 'client/index.html', {})
    
def sign_up(request):
    return render(request, 'client/register.html', {})

def register_user(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    conf_password = request.POST['conf_password']

    if password == conf_password:
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return HttpResponseRedirect(reverse('client:index'))
    else:
        return HttpResponseRedirect(reverse('client:register'))