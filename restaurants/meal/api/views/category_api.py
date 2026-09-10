"""Endpoints publics des catégories."""

from restaurants.users.api.views.api_common import CategoryListAPIView
from drf_spectacular.utils import extend_schema_view

from ..docs.category_api import category_list_doc


CategoryListAPIView = extend_schema_view(get=category_list_doc)(CategoryListAPIView)

__all__ = ["CategoryListAPIView"]
