"""Endpoints des demandes personnalisées."""

from restaurants.users.api.views.api_common import CustomOrderRequestViewSet
from drf_spectacular.utils import extend_schema_view

from ..docs.custom_request_api import custom_request_create_doc, custom_request_detail_doc, custom_request_list_doc


CustomOrderRequestViewSet = extend_schema_view(
    list=custom_request_list_doc,
    create=custom_request_create_doc,
    retrieve=custom_request_detail_doc,
)(CustomOrderRequestViewSet)

__all__ = ["CustomOrderRequestViewSet"]
