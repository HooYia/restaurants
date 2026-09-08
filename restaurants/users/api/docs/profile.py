"""Documentation Swagger de l'API du profil utilisateur."""

from drf_spectacular.utils import OpenApiResponse, extend_schema

from ..serializers.mobile_serializers import ErrorResponseSerializer, UserSerializer


PROFILE_TAG = "Profil"


profile_get_doc = extend_schema(
    tags=[PROFILE_TAG],
    summary="Consulter son profil",
    description="Retourne les informations du compte actuellement authentifié.",
    responses={
        200: OpenApiResponse(response=UserSerializer, description="Profil retourné."),
        401: OpenApiResponse(response=ErrorResponseSerializer, description="Authentification requise."),
    },
)

profile_update_doc = extend_schema(
    tags=[PROFILE_TAG],
    summary="Modifier son profil",
    description="Met à jour tout ou partie des informations du compte authentifié.",
    request=UserSerializer,
    responses={
        200: OpenApiResponse(response=UserSerializer, description="Profil mis à jour."),
        400: OpenApiResponse(response=ErrorResponseSerializer, description="Données de profil invalides."),
        401: OpenApiResponse(response=ErrorResponseSerializer, description="Authentification requise."),
    },
)
