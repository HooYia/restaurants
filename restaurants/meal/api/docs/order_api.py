"""Swagger du relais ``views/order_api.py``."""

from drf_spectacular.utils import OpenApiResponse, extend_schema

admin_order_doc = extend_schema(tags=["Administration du menu"], summary="Gérer les commandes", description="Relais documentaire pour la consultation et la mise à jour du statut des commandes.", responses={401: OpenApiResponse(description="Authentification requise."), 403: OpenApiResponse(description="Accès réservé aux administrateurs.")})
