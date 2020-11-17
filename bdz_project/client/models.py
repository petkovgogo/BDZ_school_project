from django.db import models
from django.contrib.postgres.fields import ArrayField

class Station(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Route(models.Model):
    starting_station_id = models.ForeignKey(
        Station, related_name='starting_station_id', default=None, on_delete=models.CASCADE)
    end_station_id = models.ForeignKey(
        Station, related_name='end_station_id', default=None, on_delete=models.CASCADE)
    departure_date = models.DateTimeField('departure date', default=None)
    arrival_date = models.DateTimeField('arrival date', default=None)
    duration = models.FloatField(default=0.0)
    train_id = models.IntegerField(default=0)

    def __str__(self):
        return self.starting_station_id.name + " -> " + self.end_station_id.name


class Ticket(models.Model):
    price = models.FloatField(default=0.0)
    ticket_type = models.CharField(max_length=20, default=None)
    route = models.ManyToManyField(Route, related_name='route')

    def __str__(self):
        return "Ticket: " + str(self.pk)


class Discount(models.Model):
    ticket_type = models.CharField(max_length=20)
    discount = models.FloatField(default=0.0)

    def __str__(self):
        return self.ticket_type + ' ticket\' s price = -' + (self.discount * 100) + '%'
