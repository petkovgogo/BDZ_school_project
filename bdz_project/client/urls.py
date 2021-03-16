from django.urls import path

from . import views

app_name = 'client'

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.authenticate_user, name='auth'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('buy-ticket/', views.BuyTicketView.as_view(), name='buyticket'),
    path('buy/', views.buy_ticket, name='buy'),
    path('ticket-create/', views.ticket_create, name='ticket-create'),
    path('change-credentials/', views.ChangeCredsView.as_view(), name='change-credentials'),
    path('change/', views.change_credentials, name='change'),
    path('change-successful/', views.change_successful, name='change-successful'),
]
