from rest_framework import permissions, viewsets
from drf_spectacular.utils import extend_schema_view

from restaurants.meal.models import Boisson, Meal

from ..serializers.meal import BoissonSerializer, MealSerializer
from ..docs.meal import legacy_boisson_list_doc, legacy_meal_list_doc


class AllowAnyReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]


class MealViewSet(AllowAnyReadOnlyModelViewSet):
    queryset = Meal.objects.filter(is_available=True).select_related("category").prefetch_related("accompaniments")
    serializer_class = MealSerializer


class BoissonViewSet(AllowAnyReadOnlyModelViewSet):
    queryset = Boisson.objects.filter(is_available=True)
    serializer_class = BoissonSerializer


MealViewSet = extend_schema_view(list=legacy_meal_list_doc)(MealViewSet)
BoissonViewSet = extend_schema_view(list=legacy_boisson_list_doc)(BoissonViewSet)
