from django.db import models
from users.models import User

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images/')
