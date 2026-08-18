"""Endpoints publics des boissons."""

from restaurants.users.api.views.api_common import BoissonListAPIView
from drf_spectacular.utils import extend_schema_view

from ..docs.boisson_api import boisson_list_doc


BoissonListAPIView = extend_schema_view(get=boisson_list_doc)(BoissonListAPIView)

__all__ = ["BoissonListAPIView"]
