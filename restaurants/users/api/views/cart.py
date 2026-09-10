from django.shortcuts import get_object_or_404
from rest_framework import permissions, serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurants.meal.models import Accompaniment, Boisson, Meal
from restaurants.users.cart import Cart
from ..docs.cart import (
    cart_add_boisson_doc, cart_add_doc, cart_detail_doc, cart_remove_doc,
    cart_update_component_doc, cart_update_doc,
)
from ..serializers.mobile_serializers import (
    CartAddSerializer, CartBoissonSerializer, CartComponentSerializer,
    CartResponseSerializer,
)


class CartRequestSerializer(serializers.Serializer):
    """Schéma neutre : chaque opération panier documente son propre payload."""


class CartAPIView(APIView):
    """Compatibilité avec les routes panier historiques sous ``/api/users/``.

    L'API mobile versionnée utilise la création directe de commande; ces vues
    restent disponibles pour les clients qui utilisent un panier de session.
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = CartRequestSerializer
    response_serializer_class = CartResponseSerializer

    @staticmethod
    def response(cart):
        items = []
        for item in cart:
            serialized = dict(item)
            serialized["subtotal"] = str(item["subtotal"])
            items.append(serialized)
        return Response({"items": items, "count": len(cart), "total": str(cart.get_total_price())})


class CartDetailAPIView(CartAPIView):
    @cart_detail_doc
    def get(self, request):
        return self.response(Cart(request))


class CartAddAPIView(CartAPIView):
    @cart_add_doc
    def post(self, request):
        meal = get_object_or_404(Meal, id=request.data.get("meal_id"), is_available=True)
        quantity = int(request.data.get("quantity", 1))
        if quantity < 1:
            return Response({"quantity": ["Doit être supérieur à zéro."]}, status=status.HTTP_400_BAD_REQUEST)
        accompaniments = self._accompaniments(request.data.get("accompaniments", []), meal)
        boissons = self._boissons(request.data.get("boissons", []))
        cart = Cart(request)
        cart.add(meal, quantity, accompaniments, boissons)
        return self.response(cart)

    @staticmethod
    def _accompaniments(values, meal):
        quantities = {str(value["id"]): int(value.get("quantity", 1)) for value in values}
        objects = list(Accompaniment.objects.filter(id__in=quantities))
        if len(objects) != len(quantities) or any(item not in meal.accompaniments.all() for item in objects):
            raise ValidationError({"accompaniments": "Accompagnement invalide pour ce plat."})
        return [{"accompaniment": item, "quantity": quantities[str(item.id)]} for item in objects]

    @staticmethod
    def _boissons(values):
        quantities = {str(value["id"]): int(value.get("quantity", 1)) for value in values}
        objects = list(Boisson.objects.filter(id__in=quantities, is_available=True))
        if len(objects) != len(quantities):
            raise ValidationError({"boissons": "Boisson indisponible."})
        return [{"boisson": item, "quantity": quantities[str(item.id)]} for item in objects]


class CartRemoveAPIView(CartAPIView):
    @cart_remove_doc
    def post(self, request):
        cart = Cart(request)
        cart.remove(request.data.get("item_id"))
        return self.response(cart)


class CartUpdateAPIView(CartAPIView):
    @cart_update_doc
    def post(self, request):
        quantity = int(request.data.get("quantity", 0))
        cart = Cart(request)
        cart.update_quantity(request.data.get("item_id"), quantity)
        return self.response(cart)


class CartUpdateComponentAPIView(CartAPIView):
    @cart_update_component_doc
    def post(self, request):
        component_type = request.data.get("component_type")
        if component_type not in {"accompaniment", "boisson"}:
            return Response({"component_type": ["Valeur invalide."]}, status=status.HTTP_400_BAD_REQUEST)
        cart = Cart(request)
        cart.update_component(
            request.data.get("item_id"), component_type, request.data.get("component_id"), int(request.data.get("quantity", 0))
        )
        return self.response(cart)


class CartAddBoissonAPIView(CartAPIView):
    @cart_add_boisson_doc
    def post(self, request):
        boisson = get_object_or_404(Boisson, id=request.data.get("boisson_id"), is_available=True)
        quantity = int(request.data.get("quantity", 1))
        if quantity < 1:
            return Response({"quantity": ["Doit être supérieur à zéro."]}, status=status.HTTP_400_BAD_REQUEST)
        cart = Cart(request)
        cart.add_standalone_boisson(boisson, quantity)
        return self.response(cart)
