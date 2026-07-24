from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.urls import reverse

from restaurants.users.cart import Cart
from restaurants.users.models import Address, Client
from restaurants.meal.models import Order, OrderItem, Payment, Meal, Accompaniment, Boisson
from restaurants.meal.enum import OrderStatus, PaymentMethod, PaymentStatus

class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        if len(cart) == 0:
            messages.warning(request, "Votre panier est vide.")
            return redirect('users:home')
            
        client, _ = Client.objects.get_or_create(user=request.user)
        addresses = client.addresses.all()
        
        context = {
            'cart': cart,
            'addresses': addresses,
            'delivery_fee': 1000,
        }
        return render(request, 'pages/checkout.html', context)

    def post(self, request):
        cart = Cart(request)
        if len(cart) == 0:
            return redirect('users:home')

        client, _ = Client.objects.get_or_create(user=request.user)
        
        # Address handling
        address_id = request.POST.get('address_id')
        city = request.POST.get('city')
        street = request.POST.get('street')
        description = request.POST.get('description', '')
        
        address = None
        if address_id:
            address = get_object_or_404(Address, id=address_id, client=client)
        elif city and street:
            address = Address.objects.create(
                client=client,
                city=city,
                street=street,
                description=description
            )
        else:
            messages.error(request, "Veuillez fournir une adresse de livraison valide.")
            return redirect('users:checkout')

        # Payment method
        payment_method = request.POST.get('payment_method', PaymentMethod.CASH)
        if payment_method not in dict(PaymentMethod.choices):
            payment_method = PaymentMethod.CASH

        # Create Order
        order = Order.objects.create(
            client=client,
            delivery_address=address,
            status=OrderStatus.PENDING,
            payment_method=payment_method,
            total_amount=0
        )

        # Create Order Items
        for item in cart:
            meal = Meal.objects.get(id=item['meal_id'])
            boisson = None
            if item.get('boisson'):
                boisson = Boisson.objects.filter(id=item['boisson']['id']).first()

            order_item = OrderItem.objects.create(
                order=order,
                meal=meal,
                quantity=item['quantity'],
                unit_price=meal.price,
                boisson=boisson
            )
            
            if item.get('accompaniments'):
                acc_ids = [a['id'] for a in item['accompaniments']]
                accompaniments = Accompaniment.objects.filter(id__in=acc_ids)
                order_item.accompaniments.set(accompaniments)
            
            order_item.recalculate(save=True)

        # Recalculate total with delivery fee
        order_total = order.recalculate_total(save=False)
        order.total_amount = order_total + 1000 # delivery fee
        order.save()

        # Create Payment intent
        Payment.objects.create(
            order=order,
            method=payment_method,
            status=PaymentStatus.PENDING
        )

        cart.clear()
        
        # Send Email to Admins via Celery
        try:
            from restaurants.users.tasks import send_new_order_admin_notification_task
            send_new_order_admin_notification_task.delay(order.id)
        except Exception as e:
            pass

        # Trigger success message
        messages.success(request, f"Votre commande #{order.id} a été validée avec succès !")
        return redirect('users:order-success', order_id=order.id)


class OrderSuccessView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        client, _ = Client.objects.get_or_create(user=request.user)
        order = get_object_or_404(Order, id=order_id, client=client)
        return render(request, 'pages/order_success.html', {'order': order})
