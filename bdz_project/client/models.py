from django.db import models
from django.utils import timezone
from django.conf import settings


class Schedule(models.Model):
    train_number = models.IntegerField(default=0)
    station_name = models.CharField(max_length=20)
    departure_time = models.TimeField(
        'departure time',
        default=None,
        null=True
    )

    arrival_time = models.TimeField(
        'arrival time',
        default=None,
        null=True
    )

    def __str__(self):
        if self.departure_time is None:
            return str(self.station_name) + "\n-> Arrival:  " + str(self.arrival_time)

        elif self.arrival_time is None:
            return str(self.station_name) + "\n-> Departure:  " + str(self.departure_time)

        return str(self.station_name) + "\n-> Departure:  " + str(self.departure_time) + "\n-> Arrival:  " + str(self.arrival_time)


class Station(models.Model):
    station_name = models.CharField(max_length=20)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.station_name


class TicketType(models.Model):
    ticket_type = models.CharField(max_length=20)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.ticket_type


class Ticket(models.Model):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=None, on_delete=models.CASCADE)
    ticket_type_id = models.ForeignKey(
        TicketType,
        related_name='ticket_type_id',
        default=None,
        on_delete=models.CASCADE
    )

    created_date = models.DateTimeField('created date', default=timezone.now)

    def __str__(self):
        return "Ticket id: " + str(self.pk)


class Route(models.Model):
    starting_station_id = models.ForeignKey(
        Station,
        related_name='starting_station_id',
        default=None,
        on_delete=models.CASCADE
    )

    end_station_id = models.ForeignKey(
        Station,
        related_name='end_station_id',
        default=None,
        on_delete=models.CASCADE
    )

    departure_date = models.DateTimeField('departure date', default=None)
    arrival_date = models.DateTimeField('arrival date', default=None)
    duration = models.FloatField(default=0.0)
    train_number = models.IntegerField(default=0)
    ticket_id = models.ForeignKey(
        Ticket,
        related_name='ticket_id',
        default=None,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.starting_station_id.station_name + " -> " + self.end_station_id.station_name


class Discount(models.Model):
    ticket_type = models.CharField(max_length=20)
    discount = models.FloatField(default=0.0)

    def __str__(self):
        return self.ticket_type + ' ticket\' s price = -' + (self.discount * 100) + '%'
