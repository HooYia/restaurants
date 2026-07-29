from decimal import Decimal
from django.conf import settings
from restaurants.meal.models import Meal, Accompaniment, Boisson
import uuid

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, meal, quantity=1, accompaniments_data=None, boissons_data=None):
        if accompaniments_data is None:
            accompaniments_data = []
        if boissons_data is None:
            boissons_data = []
            
        # We need a unique ID for this cart item because the same meal can be added with different options
        # We can use a combination of meal_id, sorted accompaniments, and boissons
        acc_str = "_".join([f"{a['accompaniment'].id}x{a['quantity']}" for a in sorted(accompaniments_data, key=lambda x: str(x['accompaniment'].id))])
        boisson_str = "_".join([f"{b['boisson'].id}x{b['quantity']}" for b in sorted(boissons_data, key=lambda x: str(x['boisson'].id))])
        if not acc_str: acc_str = "no_acc"
        if not boisson_str: boisson_str = "no_boi"
        
        item_id = f"{meal.id}_{acc_str}_{boisson_str}"

        # Calculate extra accompaniments fee
        extra_fee = Decimal('0.00')
        included = meal.max_included_accompaniments
        
        # Flatten accompaniments based on quantity for price sorting
        flat_accs = []
        for item in accompaniments_data:
            for _ in range(item['quantity']):
                flat_accs.append(item['accompaniment'])
                
        if len(flat_accs) > included:
            # Sort by price ascending, so the cheapest are free
            sorted_accs = sorted(flat_accs, key=lambda x: x.price)
            extra_accs = sorted_accs[included:]
            extra_fee = sum([a.price for a in extra_accs])

        boisson_price = sum([Decimal(str(b['boisson'].price)) * b['quantity'] for b in boissons_data], Decimal('0.00'))
        unit_price = meal.price
        
        # Total per unit (meal + extra accompaniments + boisson)
        total_unit_price = unit_price + extra_fee + boisson_price

        if item_id not in self.cart:
            self.cart[item_id] = {
                'quantity': 0,
                'meal_id': str(meal.id),
                'meal_name': meal.name,
                'meal_price': str(meal.price),
                'meal_image_url': meal.image.url if meal.image else "",
                'accompaniments': [{'id': str(a['accompaniment'].id), 'name': a['accompaniment'].name, 'price': str(a['accompaniment'].price), 'quantity': a['quantity']} for a in accompaniments_data],
                'boissons': [{'id': str(b['boisson'].id), 'name': b['boisson'].name, 'price': str(b['boisson'].price), 'quantity': b['quantity']} for b in boissons_data],
                'extra_fee': str(extra_fee),
                'boisson_price': str(boisson_price),
                'total_unit_price': str(total_unit_price)
            }
        
        self.cart[item_id]['quantity'] += quantity
        self.save()

    def add_standalone_boisson(self, boisson, quantity=1):
        item_id = f"boisson_{boisson.id}"
        
        unit_price = boisson.price
        total_unit_price = unit_price
        
        if item_id not in self.cart:
            self.cart[item_id] = {
                'quantity': 0,
                'is_standalone_boisson': True,
                'boisson_id': str(boisson.id),
                'meal_name': boisson.name,
                'meal_price': str(boisson.price),
                'meal_image_url': boisson.image.url if boisson.image else "",
                'accompaniments': [],
                'boissons': [],
                'extra_fee': '0.00',
                'boisson_price': str(boisson.price),
                'total_unit_price': str(total_unit_price)
            }
            
        self.cart[item_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, item_id):
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()
            
    def update_quantity(self, item_id, quantity):
        if item_id in self.cart:
            if quantity <= 0:
                self.remove(item_id)
            else:
                self.cart[item_id]['quantity'] = quantity
                self.save()

    def __iter__(self):
        for item_id, item in self.cart.items():
            item['id'] = item_id
            item['subtotal'] = Decimal(item['total_unit_price']) * item['quantity']
            yield item

    def __len__(self):
        return len(self.cart.keys())

    def get_total_price(self):
        return sum(Decimal(item['total_unit_price']) * item['quantity'] for item in self.cart.values())
        
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
