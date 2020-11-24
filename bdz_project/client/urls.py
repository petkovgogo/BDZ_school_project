from django.urls import path

from . import views

app_name = 'client'

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.authenticate_user, name='auth'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('buy-ticket/', views.BuyTicket.as_view(), name='buyticket'),
    path('buy/', views.buy_ticket, name='buy'),
]