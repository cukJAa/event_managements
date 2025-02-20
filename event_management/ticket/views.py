from django.shortcuts import render, redirect
from .models import Ticket, OrderItem
from .forms import OrderItemForm
#import qrcode 

def ticket_list(request):
    tickets = Ticket.objects.all()  
    return render(request, 'ticket_list.html', {'tickets': tickets})

def create_order(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)  
    if request.method == "POST":
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.ticket = ticket
            order_item.total_price = ticket.price * order_item.quantity  
            order_item.save()

            
            #qr = qrcode.make(f"Order: {order_item.id}")
            #qr_path = f"media/qr_codes/order_{order_item.id}.png"
            #qr.save(qr_path)
            #order_item.qr_code = qr_path
            #order_item.save()

            return redirect('order_success')  

    else:
        form = OrderItemForm()

    return render(request, 'create_order.html', {'form': form, 'ticket': ticket})

