from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from event import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('program/', views.program, name='program'),
    path('events/', views.event_list, name='events'),
    path('events/new/', views.event_create, name='event_create'),
    path('performer/', views.performer, name='performer'),
    path('ticket_details/<int:event_id>/', views.ticket_details, name='ticket_details'),
    path('', views.index, name='home'),  # Use the index view as the home view
]
