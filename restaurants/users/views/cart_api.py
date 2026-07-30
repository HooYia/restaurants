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
            accompaniments_data = []
            meal = get_object_or_404(Meal, id=meal_id, is_available=True)
            if accompaniments_list := data.get('accompaniments', []):
                acc_dict = {str(a['id']): int(a.get('quantity', 1)) for a in accompaniments_list}
                acc_objs = Accompaniment.objects.filter(id__in=acc_dict.keys())
                for obj in acc_objs:
                    accompaniments_data.append({'accompaniment': obj, 'quantity': acc_dict[str(obj.id)]})
                
            boissons_data = []
            if boissons_list := data.get('boissons', []):
                boisson_dict = {str(b['id']): int(b.get('quantity', 1)) for b in boissons_list}
                boisson_objs = Boisson.objects.filter(id__in=boisson_dict.keys(), is_available=True)
                for obj in boisson_objs:
                    boissons_data.append({'boisson': obj, 'quantity': boisson_dict[str(obj.id)]})
                
            cart.add(meal=meal, quantity=quantity, accompaniments_data=accompaniments_data, boissons_data=boissons_data)
            
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

class CartUpdateComponentView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            component_type = data.get('component_type')
            component_id = data.get('component_id')
            quantity = int(data.get('quantity', 1))
            cart.update_component(item_id, component_type, component_id, quantity)
            return JsonResponse({'status': 'success', 'cart_count': len(cart)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

class CartAddBoissonView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        try:
            data = json.loads(request.body)
            boisson_id = data.get('boisson_id')
            quantity = int(data.get('quantity', 1))
            boisson = get_object_or_404(Boisson, id=boisson_id, is_available=True)
            cart.add_standalone_boisson(boisson=boisson, quantity=quantity)
            return JsonResponse({'status': 'success', 'cart_count': len(cart)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
