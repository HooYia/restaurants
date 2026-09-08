"""
Documentation Swagger de l'API des adresses client.
"""

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from ..serializers.mobile_serializers import AddressSerializer, ErrorResponseSerializer


ADDRESS_TAG = "Adresses"


address_list_doc = extend_schema(
    tags=[ADDRESS_TAG],
    summary="Lister les adresses",
    description=(
        "Retourne la liste des adresses appartenant "
        "au client authentifié."
    ),
    responses={
        200: OpenApiResponse(response=AddressSerializer(many=True), description="Liste des adresses."),
        401: OpenApiResponse(response=ErrorResponseSerializer, description="Authentification requise."),
    },
)


address_create_doc = extend_schema(
    tags=[ADDRESS_TAG],
    summary="Créer une adresse",
    description=(
        "Crée une nouvelle adresse pour le client "
        "authentifié."
    ),
    request=AddressSerializer,
    responses={
        201: OpenApiResponse(response=AddressSerializer, description="Adresse créée."),
        400: OpenApiResponse(response=ErrorResponseSerializer, description="Données invalides."),
        401: OpenApiResponse(response=ErrorResponseSerializer, description="Authentification requise."),
    },
)


address_detail_doc = extend_schema(
    tags=[ADDRESS_TAG],
    summary="Consulter une adresse",
    description=(
        "Retourne les informations d'une adresse "
        "du client authentifié."
    ),
    responses={
        200: OpenApiResponse(response=AddressSerializer, description="Adresse retournée."),
        401: OpenApiResponse(response=ErrorResponseSerializer, description="Authentification requise."),
        404: OpenApiResponse(response=ErrorResponseSerializer, description="Adresse introuvable."),
    },
)


address_update_doc = extend_schema(
    tags=[ADDRESS_TAG],
    summary="Modifier une adresse",
    description=(
        "Modifie complètement une adresse existante."
    ),
    request=AddressSerializer,
    responses={
        200: OpenApiResponse(response=AddressSerializer, description="Adresse entièrement modifiée."),
        400: OpenApiResponse(response=ErrorResponseSerializer, description="Données invalides."),
        401: OpenApiResponse(response=ErrorResponseSerializer, description="Authentification requise."),
        404: OpenApiResponse(response=ErrorResponseSerializer, description="Adresse introuvable."),
    },
)


address_partial_update_doc = extend_schema(
    tags=[ADDRESS_TAG],
    summary="Modifier partiellement une adresse",
    description=(
        "Modifie partiellement une adresse existante."
    ),
    request=AddressSerializer,
    responses={
        200: OpenApiResponse(response=AddressSerializer, description="Adresse partiellement modifiée."),
        400: OpenApiResponse(response=ErrorResponseSerializer, description="Données invalides."),
        401: OpenApiResponse(response=ErrorResponseSerializer, description="Authentification requise."),
        404: OpenApiResponse(response=ErrorResponseSerializer, description="Adresse introuvable."),
    },
)


address_delete_doc = extend_schema(
    tags=[ADDRESS_TAG],
    summary="Supprimer une adresse",
    description=(
        "Supprime logiquement une adresse existante."
    ),
    responses={
        204: OpenApiResponse(description="Adresse supprimée logiquement."),
        401: OpenApiResponse(response=ErrorResponseSerializer, description="Authentification requise."),
        404: OpenApiResponse(response=ErrorResponseSerializer, description="Adresse introuvable."),
    },
)


address_set_default_doc = extend_schema(
    tags=[ADDRESS_TAG],
    summary="Définir une adresse par défaut",
    description=(
        "Définit l'adresse sélectionnée comme adresse "
        "par défaut du client authentifié."
    ),
    responses={
        200: OpenApiResponse(
            response=AddressSerializer,
            description="Adresse définie comme adresse par défaut.",
        ),
        401: OpenApiResponse(response=ErrorResponseSerializer, description="Authentification requise."),
        404: OpenApiResponse(response=ErrorResponseSerializer, description="Adresse introuvable."),
    },
)
