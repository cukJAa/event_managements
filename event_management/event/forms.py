from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "description", "start_time", "end_time", "location", "image"]
