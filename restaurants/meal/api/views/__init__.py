"""Views API du module meal."""

from .category import CategoryViewSet
from .meal import MealViewSet, BoissonViewSet

__all__ = ["CategoryViewSet", "MealViewSet", "BoissonViewSet"]
