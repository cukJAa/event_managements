from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

    
class User(AbstractUser):
    class Types(models.TextChoices):
        ORGANIZER = 'organizer'
        ATTENDEE = 'attendee'

    type = models.CharField(_('Type'), max_length=50, choices=Types.choices, default=Types.ATTENDEE)

    name =models.CharField(_('Name of User'), blank=True, max_length=255)
    def get_absolute_url(self):
        return reverse('user:detail', kwargs={"username": self.username})
    
    @property
    def is_organizer(self):
        return self.type == User.Types.ORGANIZER

    
class AttendeeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=User.Types.ATTENDEE)


class Attendee(User):
    objects = AttendeeManager()
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.ATTENDEE
        return super().save(*args, **kwargs)

class OrganizerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=User.Types.ORGANIZER)

class Organizer(User):
    objects = OrganizerManager()
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.ORGANIZER
        return super().save(*args, **kwargs)


