from django.contrib import admin
from django.urls import path
from event import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('program/', views.program, name='program'),
    path('venue/', views.venue, name='venue'),
    path('elements/', views.elements, name='elements'),
    path('blog/', views.blog, name='blog'),
    path('single-blog/', views.single_blog, name='single_blog'),
    path('events/', views.event_list, name='event_list'),
    path('events/new/', views.event_create, name='event_create'),
    path('', views.performer, name='performer'),
    path('', views.index, name='home'),  # Set contact view as the default
]