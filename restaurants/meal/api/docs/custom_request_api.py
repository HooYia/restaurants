"""Swagger du endpoint ``views/custom_request_api.py``."""

from drf_spectacular.utils import OpenApiResponse, extend_schema

from restaurants.users.api.serializers.mobile_serializers import (
	CustomOrderRequestSerializer,
	ErrorResponseSerializer,
)

custom_request_list_doc = extend_schema(
	tags=["Demandes sur mesure"],
	summary="Lister ses demandes sur mesure",
	description="Retourne les demandes de plats sur mesure appartenant au client authentifié.",
	responses={
		200: OpenApiResponse(response=CustomOrderRequestSerializer(many=True), description="Liste retournée."),
		401: OpenApiResponse(response=ErrorResponseSerializer, description="Authentification requise."),
	},
)
custom_request_create_doc = extend_schema(
	tags=["Demandes sur mesure"],
	summary="Créer une demande sur mesure",
	description="Crée une demande de plat hors menu pour le client authentifié.",
	request=CustomOrderRequestSerializer,
	responses={
		201: OpenApiResponse(response=CustomOrderRequestSerializer, description="Demande créée."),
		400: OpenApiResponse(response=ErrorResponseSerializer, description="Données invalides."),
		401: OpenApiResponse(response=ErrorResponseSerializer, description="Authentification requise."),
	},
)
custom_request_detail_doc = extend_schema(
	tags=["Demandes sur mesure"],
	summary="Consulter une demande sur mesure",
	description="Retourne une demande appartenant au client authentifié.",
	responses={
		200: OpenApiResponse(response=CustomOrderRequestSerializer, description="Demande retournée."),
		401: OpenApiResponse(response=ErrorResponseSerializer, description="Authentification requise."),
		404: OpenApiResponse(response=ErrorResponseSerializer, description="Demande introuvable."),
	},
)
