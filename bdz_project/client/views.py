from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

def index(request):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    return render(request, 'client/index.html', {})
=======
=======
>>>>>>> f68d3d49e57ff35f7c70ddbec17868ac5d550650
=======
>>>>>>> 1acd8453871f1046ce56f3fd4d5a7e6dff1bba2d
    return render(request, 'client/register.html', {})

def login_user(request):
    email = request.POST('email')
    password = request.POST('password')
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 0b63c8ae82d2415625b2f378e72f7fd0d15c23a9
=======
>>>>>>> f68d3d49e57ff35f7c70ddbec17868ac5d550650
=======
>>>>>>> 1acd8453871f1046ce56f3fd4d5a7e6dff1bba2d

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