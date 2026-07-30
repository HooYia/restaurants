import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from decimal import Decimal
from restaurants.meal.models import Meal, Category, Accompaniment
from django.http import HttpRequest
from django.contrib.sessions.backends.db import SessionStore
from restaurants.users.cart import Cart

meal = Meal.objects.filter(name__icontains="rognons").first()
if not meal:
    cat = Category.objects.first()
    meal = Meal.objects.create(name="Rognons test", category=cat, price=Decimal('2000.00'), max_included_accompaniments=0)

acc, _ = Accompaniment.objects.get_or_create(name="Plantain test", price=Decimal('500.00'))

request = HttpRequest()
request.session = SessionStore()

cart = Cart(request)
cart.add(meal, quantity=1, accompaniments_data=[{'accompaniment': acc, 'quantity': 1}])

item_id = list(cart.cart.keys())[0]
print("After ADD 1x Plantain (qty=1):")
for item in cart:
    print(item['quantity'], "meals. Subtotal:", item['subtotal'], "Extra Fee:", item['extra_fee'], "Total Unit Price:", item['total_unit_price'])

# Simulate clicking + on the accompaniment
cart.update_component(item_id, 'accompaniment', acc.id, 2)
item_id2 = list(cart.cart.keys())[0]

print("After update_component Plantain to 2:")
for item in cart:
    print(item['quantity'], "meals. Subtotal:", item['subtotal'], "Extra Fee:", item['extra_fee'], "Total Unit Price:", item['total_unit_price'])

# Add 2 meals
cart.update_quantity(item_id2, 2)

print("After update_quantity to 2 meals:")
for item in cart:
    print(item['quantity'], "meals. Subtotal:", item['subtotal'], "Extra Fee:", item['extra_fee'], "Total Unit Price:", item['total_unit_price'])

cart.update_component(item_id2, 'accompaniment', acc.id, 3)
print("After update_component Plantain to 3 on 2 meals:")
for item in cart:
    print(item['quantity'], "meals. Subtotal:", item['subtotal'], "Extra Fee:", item['extra_fee'], "Total Unit Price:", item['total_unit_price'])

