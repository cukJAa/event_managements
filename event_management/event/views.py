from django.shortcuts import render
from .models import Event, Location

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})

def performer(request):
    return render(request, 'performer.html')

def event_create(request):
    return render(request, 'event_create.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def program(request):
    return render(request, 'program.html')

def index(request):
    return render( request, 'index.html')
