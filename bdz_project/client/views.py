from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormView
from .forms import LoginForm, RegisterForm, RouteForm, ChangeCredentialsForm


class LoginView(FormView):
    template_name = 'client/login.html'
    form_class = LoginForm
    success_url = '/auth/'


class RegisterView(FormView):
    template_name = 'client/register.html'
    form_class = RegisterForm
    success_url = '/signup/'


class BuyTicketView(FormView):
    template_name = 'client/product.html'
    form_class = RouteForm
    success_url = '/buy/'


class ChangeCredsView(FormView):
    template_name = 'client/changeCredentials.html'
    form_class = ChangeCredentialsForm
    success_url = '/change/'

    def get_form_kwargs(self):
        kwargs = super(ChangeCredsView, self).get_form_kwargs()
        kwargs.update({'request': self.request})

        return kwargs


def index(request):
    return render(request, 'client/index.html')


def authenticate_user(request):
    form = LoginForm(request.POST)

    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=raw_password)

        if user is not None:
            login(request, user)

            return HttpResponseRedirect(reverse('client:index'))

        form.add_error('username', 'Invalid credentials')
        form.add_error('password', 'Invalid credentials')

    return render(request, 'client/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return HttpResponseRedirect(reverse('client:index'))

    return render(request, 'client/register.html', {'form': form})


def logout_view(request):
    logout(request)

    return render(request, 'client/index.html')


def buy_ticket(request):
    form = RouteForm(request.POST)

    if form.is_valid():
        return HttpResponseRedirect(reverse('client:index'))

    return render(request, 'client/product.html', {'form': form})


def change_credentials(request):
    form = ChangeCredentialsForm(request.POST, request=request)

    if form.is_valid():
        if form.cleaned_data.get('username') != "":
            request.user.username = form.cleaned_data.get('username')

        if form.cleaned_data.get('email') != "":
            request.user.email = form.cleaned_data.get('email')

        if form.cleaned_data.get('new_password') != "":
            request.user.set_password(form.cleaned_data.get('new_password'))

        request.user.save()

        return HttpResponseRedirect(reverse('client:change-successful'))

    return render(request, 'client/changeCredentials.html', {'form': form})


def change_successful(request):
    render(request, 'client/changeSuccessful.html')
