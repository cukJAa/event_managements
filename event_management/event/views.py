from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.contrib import messages
from .forms import EventForm, TicketForm
from .models import Event, Location
from ticket.models import Ticket
from datetime import datetime

def performer(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

# def event_create(request):
#     return render(request, 'event_create.html')

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

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})

def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_details.html', {'event': event})

def event_list(request):
    events = Event.objects.all()
    return render(request, "events.html", {"events": events})

@login_required
def organizer_event_list(request):
    """Display all events (attendees see all, organizers see only their own)."""
    if request.user.is_authenticated and request.user.type == "organizer":
        events = Event.objects.filter(organizer=request.user)
    else:
        events = Event.objects.none()
    
    return render(request, "event_list_organizer.html", {"events": events})


@login_required
# @permission_required("event_management.add_event", raise_exception=True)
def event_create(request):
    """Allow organizers to create an event."""
    if request.user.type != "organizer":
        messages.error(request, "Only organizers can create events.")
        return redirect("event_list")
    
    locations = Location.objects.all()

    if request.method == "POST":
        event_form = EventForm(request.POST, request.FILES)
        ticket_forms = [TicketForm(request.POST, prefix=str(i)) for i in range(3)]  # Assuming 3 ticket categories

        if event_form.is_valid() and all([tf.is_valid() for tf in ticket_forms]):
            event = event_form.save(commit=False)
            event.organizer = request.user  # Assign event to logged-in organizer
            event.save()
            for tf in ticket_forms:
                ticket = tf.save(commit=False)
                ticket.event = event
                ticket.save()
            messages.success(request, "Event and tickets created successfully!")
            return redirect(reverse("organizer_event_list"))
        else:
            print("Event form errors:", event_form.errors)  # Debugging
            for tf in ticket_forms:
                print("Ticket form errors:", tf.errors)  # Debugging
            messages.error(request, "There was an error in the form. Please fix it.")

    else:
        event_form = EventForm()
        ticket_forms = [TicketForm(prefix=str(i)) for i in range(3)]  # Assuming 3 ticket categories

    return render(request, "create_event.html", {"form": event_form, "locations": locations, 'ticket_forms': ticket_forms})



@login_required
# @permission_required("event_management.change_event", raise_exception=True)
def event_update(request, event_id):
    """Allow an organizer to edit their own event."""
    event = get_object_or_404(Event, id=event_id)
    locations = Location.objects.all()

    if request.user != event.organizer:
        messages.error(request, "You can only edit your own events.")
        return redirect("organizer_event_list")

    existing_tickets = list(event.tickets.all())  # Fetch all related tickets

    if request.method == "POST":
        event_form = EventForm(request.POST, request.FILES, instance=event)
        ticket_forms = [
            TicketForm(request.POST, prefix=str(i), instance=existing_tickets[i]) if i < len(existing_tickets) 
            else TicketForm(request.POST, prefix=str(i))  # Create new forms if fewer than 3 tickets exist
            for i in range(3)
        ]

        if event_form.is_valid() and all([tf.is_valid() for tf in ticket_forms]):
            event = event_form.save()
            for tf in ticket_forms:
                ticket = tf.save(commit=False)
                ticket.event = event
                ticket.save()
            messages.success(request, "Event and tickets updated successfully!")
            return redirect(reverse("organizer_event_list"))

    else:
        event_form = EventForm(instance=event)
        ticket_forms = [
            TicketForm(prefix=str(i), instance=existing_tickets[i]) if i < len(existing_tickets) 
            else TicketForm(prefix=str(i))  # Create empty forms if there are fewer than 3 existing tickets
            for i in range(3)
        ]
    
    return render(request, "update_event.html", {
        "form": event_form, 
        "event": event, 
        "locations": locations, 
        "ticket_forms": ticket_forms
    })
@login_required
# @permission_required("event_management.delete_event", raise_exception=True)
def event_delete(request, event_id):
    """Allow an organizer to delete their own event."""
    event = get_object_or_404(Event, id=event_id)

    if request.user != event.organizer:
        messages.error(request, "You can only delete your own events.")
        return redirect("event_list")

    event.delete()
    messages.success(request, "Event deleted successfully!")
    return redirect(reverse("organizer_event_list"))


# def create_event(request):
#     if request.method == 'POST':
#         event_form = EventForm(request.POST, request.FILES)
#         ticket_forms = [TicketForm(request.POST, prefix=str(i)) for i in range(3)]  # Assuming 3 ticket categories

#         if event_form.is_valid() and all([tf.is_valid() for tf in ticket_forms]):
#             event = event_form.save()
#             for tf in ticket_forms:
#                 ticket = tf.save(commit=False)
#                 ticket.event = event
#                 ticket.save()
#             messages.success(request, "Event and tickets created successfully!")
#             return redirect('events')
#     else:
#         event_form = EventForm()
#         ticket_forms = [TicketForm(prefix=str(i)) for i in range(3)]  # Assuming 3 ticket categories

#     return render(request, 'create_event.html', {'event_form': event_form, 'ticket_forms': ticket_forms})

def purchase_tickets(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        total_amount = 0
        tickets = []
        for ticket in event.tickets.all():
            quantity = int(request.POST.get(f'ticket_{ticket.id}', 0))
            if quantity > 0:
                total_amount += float(ticket.price) * quantity
                ticket.available_quantity -= quantity
                ticket.save()
                tickets.append({
                    'category': ticket.category,
                    'quantity': quantity,
                    'price': float(ticket.price) * quantity,
                    'event_name': event.name  # Include event name
                })
        
        # Store ticket details and total amount in session
        request.session['tickets'] = tickets
        request.session['total_amount'] = total_amount
        
        # Redirect to payment form
        return render(request, 'payment.html', {
            'event': event,
            'total_amount': total_amount,
            'tickets': tickets
        })
    return render(request, 'event/ticket_details.html', {'event': event})

def payment_success(request):
    # Retrieve the ticket details and total amount from the session
    tickets = request.session.get('tickets', [])
    total_amount = request.session.get('total_amount', 0)
    return render(request, 'payment_success.html', {
        'tickets': tickets,
        'total_amount': total_amount
    })

def my_tickets(request):
    # Retrieve the user's purchased tickets from the session or database
    tickets = request.session.get('tickets', [])
    return render(request, 'my_tickets.html', {
        'tickets': tickets
    })
