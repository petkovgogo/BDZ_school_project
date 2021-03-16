from datetime import datetime
from django.http import HttpResponseRedirect
from django.db import connection
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormView
from .forms import LoginForm, RegisterForm, RouteForm, ChangeCredentialsForm, TicketInfoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ticket, Route, TicketType, Station, Train


class LoginView(FormView):
    template_name = 'client/login.html'
    form_class = LoginForm
    success_url = '/auth/'


class RegisterView(FormView):
    template_name = 'client/register.html'
    form_class = RegisterForm
    success_url = '/signup/'


class BuyTicketView(LoginRequiredMixin, FormView):
    login_url = '/login/'
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
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=raw_password)

        if user is not None:
            login(request, user)
            nxt = request.POST.get("next")

            if nxt == '':
                return HttpResponseRedirect(reverse('client:index'))

            return redirect(nxt)

        form.add_error('username', 'Invalid credentials')
        form.add_error('password', 'Invalid credentials')

    return render(request, 'client/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.save()

            login(request, user)

            return HttpResponseRedirect(reverse('client:index'))

    return render(request, 'client/register.html', {'form': form})


def logout_view(request):
    logout(request)

    return render(request, 'client/index.html')


def buy_ticket(request):
    form = RouteForm(request.POST)

    if form.is_valid():
        query = '''
            SELECT
                st1.id AS departure_id,
	            st2.id AS arrival_id,
	            tr.id AS train_id,
	            st1.station_name AS departure, 
	            st2.station_name AS arrival, 
	            CONCAT(tr.train_type, tr.train_number) AS train,
	            tr1.departure_time,
	            tr2.arrival_time,
	            tr2.arrival_time - tr1.departure_time AS duration
            FROM client_trainstop  AS tr1 
            JOIN client_trainstop AS tr2 ON tr1.schedule_id_id = tr2.schedule_id_id
            JOIN client_schedule AS sc ON tr1.schedule_id_id = sc.id
            JOIN client_train AS tr ON sc.train_id_id = tr.id
            JOIN client_station AS st1 ON tr1.station_id_id = st1.id
            JOIN client_station AS st2 ON tr2.station_id_id = st2.id
            WHERE 
	            tr1.station_id_id = %s 
	            AND tr2.station_id_id = %s
	            AND tr2.arrival_time > tr1.departure_time
                AND %s BETWEEN sc.valid_from AND sc.valid_until
        '''

        with connection.cursor() as cursor:
            cursor.execute(
                query, [form.clean_departure_station().id,
                        form.clean_destination().id,
                        form.clean_departure_date()
                        ])

            rows = list(cursor.fetchall())
            cursor.close()

        # if len(rows) == 1:
            # return render(request, 'client/trainChoice.html', {'rows': rows, 'departure_date':form.clean_departure_date()})

        return render(request,
                      'client/trainChoice.html',
                      {'rows': rows, 'departure_date': form.clean_departure_date()}
                      )

    return render(request, 'client/product.html', {'form': form})


def ticket_create(request):
    form = TicketInfoForm(request.POST)

    if form.is_valid():
        ticket = Ticket(user=request.user,
                        ticket_type=TicketType.objects.get(
                            ticket_type='Adult'),
                        departure_date=datetime.strptime(
                            request.POST.get('departure_date'), '%Y-%m-%d')
                        )

        route = Route(
            starting_station=Station.objects.get(
                pk=request.POST.get('departure')),
            end_station=Station.objects.get(pk=request.POST.get('arrival')),
            departure_date=datetime.strptime(
                request.POST.get('departure_time'), '%H:%M'),
            arrival_date=datetime.strptime(
                request.POST.get('arrival_time'), '%H:%M'),
            duration=datetime.min + (datetime.strptime(request.POST.get('arrival_time'), '%H:%M') -
                                     datetime.strptime(request.POST.get('departure_time'), '%H:%M')),
            train=Train.objects.get(pk=request.POST.get('train')),
            ticket=ticket
        )

        ticket.save()
        route.save()

        return render(request, 'client/ticketIssue.html', {'ticket': ticket, 'route': route})


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
    return render(request, 'client/changeSuccessful.html')
