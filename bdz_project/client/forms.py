import datetime
from django import forms
from .models import Station, TicketType
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(label='Enter your username', max_length=100)
    password = forms.CharField(label='Enter your password',
                               max_length=100, min_length=8, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        label='Enter your first name', max_length=100, required=False)
    last_name = forms.CharField(
        label='Enter your last name', max_length=100, required=False)
    username = forms.CharField(label='Enter your username', max_length=100)
    email = forms.EmailField(label='Enter your email', max_length=100)
    password = forms.CharField(label='Enter your password',
                               max_length=100, min_length=8, widget=forms.PasswordInput)
    conf_password = forms.CharField(label='Confirm your password',
                                    max_length=100, min_length=8, widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('conf_password')

        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password']
        )
        return user


class BuyTicketForm(forms.Form):
    departure_date = forms.DateField(label='Choose a departure date',
                                     initial=datetime.date.today().strftime('%d.%m.%Y'),
                                     input_formats=['%d.%m.%Y'],
                                     widget=forms.DateInput(attrs={'class': 'date-picker'}))
    arrival_date = forms.DateField(label='Choose an arrival date',
                                   required=False,
                                   input_formats=['%d.%m.%Y'],
                                   widget=forms.DateInput(attrs={'placeholder': 'oneway', 'class': 'date-picker'}))
    ticket_type = forms.ModelChoiceField(
        label='Choose a ticket type', queryset=TicketType.objects.order_by('ticket_type').all())
    departure_station = forms.ModelChoiceField(
        label='Choose a departure station', queryset=Station.objects.order_by('station_name').all())
    destination = forms.ModelChoiceField(
        label='Choose a destination', queryset=Station.objects.order_by('station_name').all())

    def clean_departure_date(self):
        departure_date = str(self.cleaned_data.get('departure_date'))
        curr_date = str(datetime.date.today())
        if departure_date < curr_date:
            raise forms.ValidationError("Departure date cannot be in the past")
        return departure_date

    def clean_arrival_date(self):
        departure_date = self.cleaned_data.get('departure_date')
        arrival_date = self.cleaned_data.get('arrival_date')

        if arrival_date is None:
            return departure_date

        if str(departure_date) <= str(arrival_date):
            raise forms.ValidationError(
                "Arrival date cannot be before departure date")
        return departure_date
