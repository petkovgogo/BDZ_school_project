from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def index(request):
    return HttpResponse('Hello')

def register_user(request):
    first_name = request.POST('first_name')
    last_name = request.POST('last_name')
    username = request.POST('username')
    email = request.POST('email')
    password = request.POST('password')
    conf_password = request.POST('conf_password')

    if password == conf_password:
        user = User.objects.create(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return HttpResponseRedirect(reverse('client:index'))
    else:
        return HttpResponseRedirect(reverse('client:register'))