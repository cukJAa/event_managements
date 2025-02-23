from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .forms import EventForm, TicketForm
from .models import Event, Location
from ticket.models import Ticket
from datetime import datetime

def event_list(request):
    """Display all events (attendees see all, organizers see only their own)."""
    if request.user.is_authenticated and request.user.type == "organizer":
        events = Event.objects.filter(organizer=request.user)
    else:
        events = Event.objects.all()
    
    return render(request, "events.html", {"events": events})

def performer(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

@login_required
@permission_required("event_management.add_event", raise_exception=True)
def event_create(request):
    """Allow organizers to create an event."""
    if request.user.type != "organizer":
        messages.error(request, "Only organizers can create events.")
        return redirect("events")

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # Assign event to logged-in organizer
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect("events")
    else:
        form = EventForm()
    
    return render(request, "event_create.html", {"form": form})

@login_required
@permission_required("event_management.change_event", raise_exception=True)
def event_update(request, event_id):
    """Allow an organizer to edit their own event."""
    event = get_object_or_404(Event, id=event_id)

    if request.user != event.organizer:
        messages.error(request, "You can only edit your own events.")
        return redirect("events")

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect("events")
    else:
        form = EventForm(instance=event)
    
    return render(request, "event_create.html", {"form": form})

@login_required
@permission_required("event_management.delete_event", raise_exception=True)
def event_delete(request, event_id):
    """Allow an organizer to delete their own event."""
    event = get_object_or_404(Event, id=event_id)

    if request.user != event.organizer:
        messages.error(request, "You can only delete your own events.")
        return redirect("events")

    event.delete()
    messages.success(request, "Event deleted successfully!")
    return redirect("events")

def ticket_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'ticket_details.html', {'event': event})

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def index(request):
    return render(request, 'index.html')

def home(request):
    events = Event.objects.all()
    return render(request, 'index.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})

def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_details.html', {'event': event})

def create_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES)
        ticket_forms = [TicketForm(request.POST, prefix=str(i)) for i in range(3)]  # Assuming 3 ticket categories

        if event_form.is_valid() and all([tf.is_valid() for tf in ticket_forms]):
            event = event_form.save()
            for tf in ticket_forms:
                ticket = tf.save(commit=False)
                ticket.event = event
                ticket.save()
            messages.success(request, "Event and tickets created successfully!")
            return redirect('events')
    else:
        event_form = EventForm()
        ticket_forms = [TicketForm(prefix=str(i)) for i in range(3)]  # Assuming 3 ticket categories

    return render(request, 'create_event.html', {'event_form': event_form, 'ticket_forms': ticket_forms})
