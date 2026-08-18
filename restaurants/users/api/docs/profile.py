"""Documentation Swagger de l'API du profil utilisateur."""

from drf_spectacular.utils import OpenApiResponse, extend_schema


PROFILE_TAG = "Profil"


profile_get_doc = extend_schema(
    tags=[PROFILE_TAG],
    summary="Consulter son profil",
    description="Retourne les informations du compte actuellement authentifié.",
    responses={401: OpenApiResponse(description="Authentification requise.")},
)

profile_update_doc = extend_schema(
    tags=[PROFILE_TAG],
    summary="Modifier son profil",
    description="Met à jour tout ou partie des informations du compte authentifié.",
    responses={400: OpenApiResponse(description="Données de profil invalides.")},
)
