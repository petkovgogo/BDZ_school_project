from django.db import models

class Route(models.Model):
    starting_station = models.CharField(max_length=100)
    end_station = models.CharField(max_length=100)
    
    def __str__(self):
        self.starting_station + " -> " + self.end_station

class Ticket(models.Model):
    price = models.FloatField(default=0.0)
    departure_date = models.DateTimeField('departure date')
    train_id = models.IntegerField(default=0)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.route