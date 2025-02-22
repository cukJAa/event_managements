from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from event import views
from .views import event_list, event_create, event_update, event_delete, event_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('program/', views.program, name='program'),
    path('events/', views.event_list, name='events'),
    path('events/new/', views.event_create, name='event_create'),
    path('performer/', views.performer, name='performer'),

    path('', views.index, name='home'),  
    path("events/", event_list, name="event_list"),
    path("events/create/", event_create, name="event_create"),
    path("events/update/<int:event_id>/", event_update, name="event_update"),
    path("events/delete/<int:event_id>/", event_delete, name="event_delete"),
    path("events/", event_list, name="event_list"),
    path("events/create/", event_create, name="event_create"),
    path("events/<int:event_id>/", event_detail, name="event_detail"),
    path('ticket/<int:event_id>/', views.ticket_details, name='ticket_details'),
    path('', views.home, name='home'),  # Use the home view as the home view
    path('event/<int:event_id>/', views.event_details, name='event_details'),
]

