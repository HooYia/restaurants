from rest_framework import permissions, viewsets
from drf_spectacular.utils import extend_schema_view

from restaurants.meal.models import Category

from ..serializers.category import CategorySerializer
from ..docs.category import legacy_category_list_doc


class AllowAnyReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]


class CategoryViewSet(AllowAnyReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by("display_order", "name")
    serializer_class = CategorySerializer


CategoryViewSet = extend_schema_view(list=legacy_category_list_doc)(CategoryViewSet)
