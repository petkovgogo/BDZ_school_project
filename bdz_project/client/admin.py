from django.contrib import admin
from .models import TicketType, Station, Discount, Schedule, Train, TrainStop

admin.site.register(TicketType)
admin.site.register(Station)
admin.site.register(Discount)
admin.site.register(Schedule)
admin.site.register(Train)
admin.site.register(TrainStop)
