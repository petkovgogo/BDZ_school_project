import datetime
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import Station

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Enter your username:',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

    password = forms.CharField(
        label='Enter your password:',
        max_length=30,
        min_length=8,
        required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        label='Enter your first name',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

    last_name = forms.CharField(
        label='Enter your last name',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

    username = forms.CharField(
        label='Enter your username',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

    email = forms.EmailField(
        label='Enter your email',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

    password = forms.CharField(
        label='Enter your password',
        max_length=30,
        min_length=8,
        required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )

    conf_password = forms.CharField(
        label='Confirm your password',
        max_length=30,
        min_length=8,
        required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username is None or username == '':
            raise forms.ValidationError('Username cannot be empty')

        username_check = User.objects.filter(username=username)

        if username_check.count():
            raise forms.ValidationError('Username already exists')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email is None or email == '':
            raise forms.ValidationError('Email cannot be empty')

        password = User.objects.filter(email=email)

        if password.count():
            raise forms.ValidationError('Email already exists')

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if password is None or password == '':
            raise forms.ValidationError('Password cannot be empty')

        return password

    def clean_conf_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('conf_password')

        if password2 is None or password2 == '':
            raise forms.ValidationError('Confirm password cannot be empty')

        if password1 != password2:
            raise forms.ValidationError('Passwords do not match')

        return password2

    def save(self):
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password')
        )

        return user


class RouteForm(forms.Form):
    departure_date = forms.DateField(
        label='Choose a departure date',
        initial=datetime.date.today().strftime('%d.%m.%Y'),
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(
            attrs={'class': 'date-picker', 'autocomplete': 'off'}),
        required=False
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

    def clean_departure_date(self):
        departure_date = self.cleaned_data.get('departure_date')

        if departure_date is None:
            raise forms.ValidationError('You must pick a departure date')

        curr_date = datetime.date.today()

        if departure_date < curr_date:
            raise forms.ValidationError('Departure date cannot be in the past')

        return departure_date

    def clean_departure_station(self):
        departure_station = self.cleaned_data.get('departure_station')

        if departure_station is None:
            raise forms.ValidationError('You must pick a departure station')

        return departure_station

    def clean_destination(self):
        destination = self.cleaned_data.get('destination')

        if destination is None:
            raise forms.ValidationError('You must pick a destination')

        return destination


class ChangeCredentialsForm(forms.Form):
    curr_password = forms.CharField(
        label='Enter your current password',
        max_length=30,
        min_length=8,
        required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )

    new_password = forms.CharField(
        label='Enter your new password',
        max_length=30,
        min_length=8,
        required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.user = self.request.user
        super(ChangeCredentialsForm, self).__init__(*args, **kwargs)

    def clean_curr_password(self):
        curr_password = self.cleaned_data.get('curr_password')

        if curr_password != "":
            tmp_user = authenticate(
                username=self.user.username, password=curr_password)

            if tmp_user is None:
                raise forms.ValidationError('Invalid password')

        return curr_password

    def clean_new_password(self):
        curr_password = self.cleaned_data.get('curr_password')

        if curr_password != "":
            new_password = self.cleaned_data.get('new_password')

            if new_password == curr_password:
                raise forms.ValidationError('New password must be different')

        return curr_password


class TicketInfoForm(forms.Form):
    train = forms.CharField(
        max_length=10,
        required=True
    )

    departure = forms.IntegerField(
        required=True
    )

    arrival = forms.IntegerField(
        required=True
    )

    departure_time = forms.TimeField(
        required=True
    )

    arrival_time = forms.TimeField(
        required=True
    )

    departure_date = forms.DateField(
        required=True
    )
