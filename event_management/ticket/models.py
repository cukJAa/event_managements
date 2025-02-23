from django.db import models
from event.models import Event  # Import the Event model

class Ticket(models.Model):
    NORMAL = 'Normal'
    GOLD = 'Gold'
    VIP = 'VIP'
    
    CATEGORY_CHOICES = [
        (NORMAL, 'Normal'),
        (GOLD, 'Gold'),
        (VIP, 'VIP'),
    ]
    
    event = models.ForeignKey(Event, related_name='tickets', on_delete=models.CASCADE)  # Add foreign key to Event
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default=NORMAL)  
    price = models.DecimalField(max_digits=8, decimal_places=2)  
    available_quantity = models.PositiveIntegerField()  
    # qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)  

    objects = models.Manager()

    def __str__(self):
        return f"{self.category} - {self.price}"
    

class OrderItem(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField()  
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  

    def save(self, *args, **kwargs):
        self.total_price = self.ticket.price * self.quantity  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order for {self.quantity} tickets: {self.ticket.category}"


