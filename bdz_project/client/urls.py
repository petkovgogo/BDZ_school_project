from django.urls import path

from . import views

app_name = 'client'

urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register')
]