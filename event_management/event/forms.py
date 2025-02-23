from django import forms
from .models import Event
from ticket.models import Ticket

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'start_time', 'end_time', 'location', 'organizer', 'image']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['category', 'price', 'available_quantity']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['category', 'price', 'available_quantity']