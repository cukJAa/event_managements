from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.contenttypes.models import ContentType
from event.models import Event
from django.contrib.auth.models import Permission
from django.contrib.auth import logout as auth_logout
# from django.contrib.auth import get_user_model

# User = get_user_model

def user_create(request):
    return render(request, 'register.html')

def signup(request):
    """
    Registration view for attendees (users).
    This view creates a new user with the role set to 'attendee'.
    """
    if request.method == "POST":
        # Get form data from the POST request
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email").strip().lower()
        password = request.POST.get("password")
        
        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered. Please log in.")
            return redirect(reverse("user_login"))
        
        # Create the user using the custom manager which auto-assigns username = email.
        user = User.objects.create_user(email=email, username=email, password=password, first_name=first_name, last_name=last_name)
        # Set the role to 'attendee'
        user.role = "attendee"
        user.save()

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
        
        messages.success(request, "Registration successful!")
        return redirect(reverse("home"))
    else:
        messages.error(request, "Invalid request method.")
        return render(request, "register.html")
    

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("email").strip().lower()
        password = request.POST.get("password")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            auth_login(request, user)  # Log the user in
            messages.success(request, "Login successful!")
            return redirect(reverse("home"))  # Redirect to home page
        else:
            messages.error(request, "Invalid email or password.")
            return redirect(reverse("user_login"))  # Redirect back to login

    return render(request, 'login.html')

def user_logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect(reverse("home"))

def signup_as_organizer(request):
    """
    Registration view for attendees (users).
    This view creates a new user with the role set to 'attendee'.
    """
    if request.method == "POST":
        # Get form data from the POST request
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email").strip().lower()
        password = request.POST.get("password")
        
        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered. Please log in.")
            return redirect(reverse("login_as_organizer"))
        
        # Create the user using the custom manager which auto-assigns username = email.
        user = User.objects.create_user(email=email, username=email, password=password, first_name=first_name, last_name=last_name)
        # Set the role to 'organizer'
        user.type = User.Types.ORGANIZER
        user.save(update_fields=["type"])

        content_type = ContentType.objects.get_for_model(Event)
        permissions = Permission.objects.filter(content_type=content_type)
        user.user_permissions.add(*permissions)

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
        
        messages.success(request, "Registration successful!")
        return redirect(reverse("home"))
    else:
        messages.error(request, "Invalid request method.")
        return render(request, "register_as_organizer.html")
    
def organizer_login(request):
    if request.method == "POST":
        username = request.POST.get("email").strip().lower()
        password = request.POST.get("password")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            auth_login(request, user)  # Log the user in
            messages.success(request, "Login successful!")
            return redirect(reverse("home"))  # Redirect to home page
        else:
            messages.error(request, "Invalid email or password.")
            return redirect(reverse("organizer_login"))  # Redirect back to login

    return render(request, 'login_as_organizer.html')

def organizer_logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect(reverse('home'))