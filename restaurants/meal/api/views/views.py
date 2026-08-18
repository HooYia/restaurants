from rest_framework import permissions, viewsets
from drf_spectacular.utils import extend_schema_view

from restaurants.meal.models import Boisson, Category, Meal

from ..serializers.serializers import BoissonSerializer, CategorySerializer, MealSerializer
from ..docs.views import legacy_views_doc


class AllowAnyReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]


class CategoryViewSet(AllowAnyReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by("display_order", "name")
    serializer_class = CategorySerializer


class MealViewSet(AllowAnyReadOnlyModelViewSet):
    queryset = Meal.objects.filter(is_available=True).select_related("category").prefetch_related("accompaniments")
    serializer_class = MealSerializer


class BoissonViewSet(AllowAnyReadOnlyModelViewSet):
    queryset = Boisson.objects.filter(is_available=True)
    serializer_class = BoissonSerializer


CategoryViewSet = extend_schema_view(list=legacy_views_doc)(CategoryViewSet)
MealViewSet = extend_schema_view(list=legacy_views_doc)(MealViewSet)
BoissonViewSet = extend_schema_view(list=legacy_views_doc)(BoissonViewSet)
