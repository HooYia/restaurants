"""Endpoints des accompagnements."""

from .admin_api import AdminAccompanimentViewSet
from drf_spectacular.utils import extend_schema_view

from ..docs.accompaniment_api import admin_accompaniment_doc


AdminAccompanimentViewSet = extend_schema_view(
    list=admin_accompaniment_doc,
    retrieve=admin_accompaniment_doc,
    create=admin_accompaniment_doc,
    update=admin_accompaniment_doc,
    partial_update=admin_accompaniment_doc,
    destroy=admin_accompaniment_doc,
)(AdminAccompanimentViewSet)

__all__ = ["AdminAccompanimentViewSet"]
