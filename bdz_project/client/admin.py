from django.contrib import admin
from .models import TicketType, Station, Discount, Ticket, Route

admin.site.register(TicketType)
admin.site.register(Station)
admin.site.register(Discount)
