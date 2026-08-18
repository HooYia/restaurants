"""Endpoints des commandes du restaurant."""

from .admin_api import AdminOrderViewSet as OrderViewSet
from drf_spectacular.utils import extend_schema_view

from ..docs.order_api import admin_order_doc


OrderViewSet = extend_schema_view(
    list=admin_order_doc,
    retrieve=admin_order_doc,
    partial_update=admin_order_doc,
)(OrderViewSet)

__all__ = ["OrderViewSet"]
