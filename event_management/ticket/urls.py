from django.urls import path
from . import views  

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),  
    path('order/<int:ticket_id>/', views.create_order, name='create_order'),  
]
