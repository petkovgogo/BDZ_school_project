import datetime
from django import forms
from django.contrib.auth.models import User
from .models import Station


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Enter your username',
        max_length=100,
        widget=forms.TextInput(attrs={'autocomplete': 'chrome-off'})
    )

    password = forms.CharField(
        label='Enter your password',
        max_length=100,
        min_length=8,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        label='Enter your first name',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'chrome-off'})
    )

    last_name = forms.CharField(
        label='Enter your last name',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'chrome-off'})
    )

    username = forms.CharField(
        label='Enter your username',
        max_length=100,
        widget=forms.TextInput(attrs={'autocomplete': 'chrome-off'})
    )

    email = forms.EmailField(
        label='Enter your email',
        max_length=100,
        widget=forms.TextInput(attrs={'autocomplete': 'chrome-off'})
    )

    password = forms.CharField(
        label='Enter your password',
        max_length=100, min_length=8,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )

    conf_password = forms.CharField(
        label='Confirm your password',
        max_length=100,
        min_length=8,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        username = User.objects.filter(username=username)

        if username.count():
            raise forms.ValidationError("Username already exists")

        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        password = User.objects.filter(email=email)

        if password.count():
            raise forms.ValidationError("Email already exists")

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('conf_password')

        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password']
        )

        return user


class RouteForm(forms.Form):
    departure_date = forms.DateField(
        label='Choose a departure date',
        initial=datetime.date.today().strftime('%d.%m.%Y'),
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(attrs={'class': 'date-picker'}),
        required=False
    )

    arrival_date = forms.DateField(
        label='Choose an arrival date',
        required=False,
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(
            attrs={'placeholder': 'oneway', 'class': 'date-picker'})
    )

    departure_station = forms.ModelChoiceField(
        label='Choose a departure station',
        queryset=Station.objects.order_by('station_name').all(),
        required=False
    )

    destination = forms.ModelChoiceField(
        label='Choose a destination',
        queryset=Station.objects.order_by('station_name').all(),
        required=False
    )

    departure_time = forms.TimeField(
        label='Departure after',
        widget=forms.TimeInput(format='%H:%M', attrs={'class': 'time-picker'}),
        required=False
    )

    def clean_departure_date(self):
        departure_date = self.cleaned_data.get('departure_date')

        if departure_date is None:
            raise forms.ValidationError("You must pick a departure date")

        curr_date = str(datetime.date.today())

        if str(departure_date) < curr_date:
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

    def clean_departure_station(self):
        departure_station = self.cleaned_data.get('departure_station')

        if departure_station is None:
            raise forms.ValidationError("You must pick a departure station")

        return departure_station

    def clean_destination(self):
        destination = self.cleaned_data.get('destination')

        if destination is None:
            raise forms.ValidationError("You must pick a destination")

        return destination

    def clean_departure_time(self):
        departure_time = self.cleaned_data.get('departure_time')

        if departure_time is None:
            raise forms.ValidationError("You must pick a departure time")

        return departure_time
