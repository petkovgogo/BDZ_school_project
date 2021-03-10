from django.db import models
from django.utils import timezone
from django.conf import settings


class Train(models.Model):
    train_number = models.PositiveSmallIntegerField(default=0)
    train_type = models.CharField(max_length=10)

    def __str__(self):
        return self.train_type + ' ' + str(self.train_number)


class Station(models.Model):
    station_name = models.CharField(max_length=20)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.station_name


class Schedule(models.Model):
    train_id = models.ForeignKey(
        Train,
        default=None,
        on_delete=models.CASCADE
    )

    week_days = models.PositiveSmallIntegerField(default=127)
    valid_from = models.DateField('valid from', default=None)
    valid_until = models.DateField('valid until', default=None, null=True)

    def __str__(self):
        return str(self.train_id)


class TrainStop(models.Model):
    schedule_id = models.ForeignKey(
        Schedule,
        default=None,
        on_delete=models.CASCADE
    )

    station_id = models.ForeignKey(
        Station,
        default=None,
        on_delete=models.CASCADE
    )

    departure_time = models.TimeField(
        'departure time',
        default=None,
        null=True,
        blank=True
    )

    arrival_time = models.TimeField(
        'arrival time',
        default=None,
        null=True,
        blank=True
    )

    def __str__(self):
        if self.departure_time is None:
            return (str(self.schedule_id) + ": " + str(self.station_id.station_name) +
                    "\n-> Arrival: " + str(self.arrival_time))

        if self.arrival_time is None:
            return (str(self.schedule_id) + ": " + str(self.station_id.station_name) +
                    "\n-> Departure: " + str(self.departure_time))

        return (str(self.schedule_id) + ": " + 
                str(self.station_id.station_name) + "\n-> Departure: " +
                str(self.departure_time) + "\n-> Arrival:  " + str(self.arrival_time))


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
        default=None,
        on_delete=models.CASCADE
    )

    created_date = models.DateTimeField('created date', default=timezone.now)

    def __str__(self):
        return "Ticket id: " + str(self.pk)


class Route(models.Model):
    starting_station_id = models.ForeignKey(
        Station,
        related_name='start_station',
        default=None,
        on_delete=models.CASCADE
    )

    end_station_id = models.ForeignKey(
        Station,
        related_name='end_station',
        default=None,
        on_delete=models.CASCADE
    )

    departure_date = models.DateTimeField('departure date', default=None)
    arrival_date = models.DateTimeField('arrival date', default=None)
    duration = models.FloatField(default=0.0)
    train_id = models.ForeignKey(
        Train,
        default=None,
        on_delete=models.CASCADE
    )

    ticket_id = models.ForeignKey(
        Ticket,
        default=None,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.starting_station_id.station_name + " -> " + self.end_station_id.station_name


class Discount(models.Model):
    ticket_type_id = models.ForeignKey(
        TicketType,
        default=None,
        on_delete=models.CASCADE
    )
    discount = models.FloatField(default=0.0)

    def __str__(self):
        return self.ticket_type_id.ticket_type + ' ticket\' s price = -' + (self.discount * 100) + '%'
