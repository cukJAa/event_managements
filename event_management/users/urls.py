from django.urls import path
from . import views

urlpatterns = [
    path('register', views.user_create, name="user_create"),
    path('signup', views.signup, name='signup'),
    path('login', views.user_login, name='user_login'),
    path('signup/organizer', views.signup_as_organizer, name='signup_as_organizer'),
    path('signup/organizer/login', views.organizer_login, name='organizer_login'),
    
]