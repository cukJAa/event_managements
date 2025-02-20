from django.db import models

from django.db import models

class Ticket(models.Model):
    category = models.CharField(max_length=100)  
    price = models.DecimalField(max_digits=8, decimal_places=2)  
    available_quantity = models.PositiveIntegerField()  
    #qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)  

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


