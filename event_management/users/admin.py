from django.contrib import admin
from .models import User, Attendee, Organizer

admin.site.register(User)
admin.site.register(Attendee)
admin.site.register(Organizer)
