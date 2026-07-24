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

    def add(self, meal, quantity=1, accompaniments=None, boisson=None):
        if accompaniments is None:
            accompaniments = []
            
        # We need a unique ID for this cart item because the same meal can be added with different options
        # We can use a combination of meal_id, sorted accompaniments, and boisson_id
        acc_str = "_".join([str(a.id) for a in sorted(accompaniments, key=lambda x: str(x.id))])
        boisson_str = str(boisson.id) if boisson else "none"
        item_id = f"{meal.id}_{acc_str}_{boisson_str}"

        # Calculate extra accompaniments fee
        extra_fee = Decimal('0.00')
        included = meal.max_included_accompaniments
        if len(accompaniments) > included:
            # Sort by price ascending, so the cheapest are free
            sorted_accs = sorted(accompaniments, key=lambda x: x.price)
            extra_accs = sorted_accs[included:]
            extra_fee = sum([a.price for a in extra_accs])

        boisson_price = boisson.price if boisson else Decimal('0.00')
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
                'accompaniments': [{'id': str(a.id), 'name': a.name, 'price': str(a.price)} for a in accompaniments],
                'boisson': {'id': str(boisson.id), 'name': boisson.name, 'price': str(boisson.price)} if boisson else None,
                'extra_fee': str(extra_fee),
                'boisson_price': str(boisson_price),
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
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['total_unit_price']) * item['quantity'] for item in self.cart.values())
        
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
