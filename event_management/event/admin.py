from django.contrib import admin
from .models import Event, Location, EventImage
from ticket.models import Ticket

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1

class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1

class EventAdmin(admin.ModelAdmin):
    inlines = [EventImageInline, TicketInline]

admin.site.register(Event, EventAdmin)
admin.site.register(Location)