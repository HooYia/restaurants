"""Swagger du relais ``views/accompaniment_api.py``."""

from drf_spectacular.utils import OpenApiResponse, extend_schema

admin_accompaniment_doc = extend_schema(tags=["Administration du menu"], summary="Gérer les accompagnements", description="Relais documentaire pour la gestion administrateur des accompagnements.", responses={401: OpenApiResponse(description="Authentification requise."), 403: OpenApiResponse(description="Accès réservé aux administrateurs.")})
