"""Endpoints publics des repas."""

from restaurants.users.api.views.api_common import MealViewSet
from drf_spectacular.utils import extend_schema_view

from ..docs.meal_api import meal_detail_doc, meal_list_doc


MealViewSet = extend_schema_view(list=meal_list_doc, retrieve=meal_detail_doc)(MealViewSet)

__all__ = ["MealViewSet"]
