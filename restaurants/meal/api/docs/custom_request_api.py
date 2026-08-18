"""Swagger du endpoint ``views/custom_request_api.py``."""

from drf_spectacular.utils import OpenApiResponse, extend_schema

custom_request_list_doc = extend_schema(tags=["Demandes sur mesure"], summary="Lister ses demandes sur mesure", description="Retourne les demandes de plats sur mesure appartenant au client authentifié.", responses={401: OpenApiResponse(description="Authentification requise.")})
custom_request_create_doc = extend_schema(tags=["Demandes sur mesure"], summary="Créer une demande sur mesure", description="Crée une demande de plat hors menu pour le client authentifié.", responses={201: OpenApiResponse(description="Demande créée."), 400: OpenApiResponse(description="Données invalides."), 401: OpenApiResponse(description="Authentification requise.")})
custom_request_detail_doc = extend_schema(tags=["Demandes sur mesure"], summary="Consulter une demande sur mesure", description="Retourne une demande appartenant au client authentifié.", responses={404: OpenApiResponse(description="Demande introuvable.")})
