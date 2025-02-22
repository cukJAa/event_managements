from django.shortcuts import render, get_object_or_404
from .models import Event, Location
from datetime import datetime

def event_list(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

def performer(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

def event_create(request):
    return render(request, 'event_create.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def program(request):
    events = Event.objects.all()
    print(events)  # Debugging statement
    return render(request, 'program.html', {'events': events})

def index(request):
    return render( request, 'index.html')

def ticket_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'ticket_details.html', {'event': event})

def home(request):
    events = Event.objects.all()
    return render(request, 'index.html', {'events': events})

def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_details.html', {'event': event})
