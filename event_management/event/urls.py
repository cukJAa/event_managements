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
    path('performer/', views.performer, name='performer'),
    path('events/', views.event_list, name='events'),
    path('events/event_list', views.organizer_event_list, name='organizer_event_list'),
    path('events/new/', views.event_create, name='event_create'),
    path('events/update/<int:event_id>/', views.event_update, name='event_update'),
    path('events/delete/<int:event_id>/', views.event_delete, name='event_delete'),
    path('events/<int:event_id>/', views.event_details, name='event_detail'),
    path('ticket/<int:event_id>/', views.ticket_details, name='ticket_details'),
    path('', views.home, name='home'),  # Use the home view as the home view
    path('event/<int:event_id>/', views.event_details, name='event_details'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
