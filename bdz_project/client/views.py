from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

def index(request):
    return render(request, 'client/index.html', {})
    
def login_user(request):
    email = request.POST['email']
    password = request.POST['password']
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