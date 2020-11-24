from django.urls import path

from . import views

app_name = 'client'

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.authenticate_user, name='auth'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('buy-ticket/', views.BuyTicket.as_view(), name='buyticket'),
    path('buy/', views.buy_ticket, name='buy'),
]