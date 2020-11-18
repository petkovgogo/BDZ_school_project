from django.urls import path

from . import views

app_name = 'client'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('auth/', views.authenticate_user, name='auth'),
    
]