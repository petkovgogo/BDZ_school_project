from django.contrib import admin
from .models import TicketType, Station, Discount

admin.site.register(TicketType)
admin.site.register(Station)
admin.site.register(Discount)
