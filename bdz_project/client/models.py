from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Station(models.Model):
    station_name = models.CharField(max_length=20)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.station_name

class TicketType(models.Model):
    ticket_type = models.CharField(max_length=20)
    
    def __str__(self):
        return 'Ticket type: ' + self.ticket_type

class Ticket(models.Model):
    user_id = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    price = models.FloatField(default=0.0)
    ticket_type_id = models.ForeignKey(TicketType, related_name='ticket_type_id', default=None, on_delete=models.CASCADE)
    created_date = models.DateTimeField('created date', default=timezone.now)

    def __str__(self):
        return "Ticket id: " + str(self.pk)

class Route(models.Model):
    starting_station_id = models.ForeignKey(
        Station, related_name='starting_station_id', default=None, on_delete=models.CASCADE)
    end_station_id = models.ForeignKey(
        Station, related_name='end_station_id', default=None, on_delete=models.CASCADE)
    departure_date = models.DateTimeField('departure date', default=None)
    arrival_date = models.DateTimeField('arrival date', default=None)
    duration = models.FloatField(default=0.0)
    train_id = models.IntegerField(default=0)
    ticket_id = models.ForeignKey(Ticket, related_name='ticket_id', default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.starting_station_id.name + " -> " + self.end_station_id.name

class Discount(models.Model):
    ticket_type = models.CharField(max_length=20)
    discount = models.FloatField(default=0.0)

    def __str__(self):
        return self.ticket_type + ' ticket\' s price = -' + (self.discount * 100) + '%'
