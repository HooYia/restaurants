import json
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from restaurants.meal.models import Meal, Accompaniment, Boisson
from restaurants.users.cart import Cart

class CartAddView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        try:
            data = json.loads(request.body)
            meal_id = data.get('meal_id')
            quantity = int(data.get('quantity', 1))
            accompaniment_ids = data.get('accompaniments', [])
            boisson_id = data.get('boisson_id')
            
            meal = get_object_or_404(Meal, id=meal_id, is_available=True)
            
            accompaniments = []
            if accompaniment_ids:
                accompaniments = list(Accompaniment.objects.filter(id__in=accompaniment_ids))
                
            boisson = None
            if boisson_id:
                boisson = Boisson.objects.filter(id=boisson_id, is_available=True).first()
                
            cart.add(meal=meal, quantity=quantity, accompaniments=accompaniments, boisson=boisson)
            
            return JsonResponse({'status': 'success', 'cart_count': len(cart)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


class CartRemoveView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            cart.remove(item_id)
            return JsonResponse({'status': 'success', 'cart_count': len(cart)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


class CartUpdateView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            quantity = int(data.get('quantity', 1))
            cart.update_quantity(item_id, quantity)
            return JsonResponse({'status': 'success', 'cart_count': len(cart)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
