"""
Documentation Swagger de l'API des paramètres de présentation
du restaurant.
"""

from drf_spectacular.utils import extend_schema, OpenApiResponse


COMPANY_SETTING_TAG = "Paramètres du restaurant"


company_setting_get_doc = extend_schema(
    tags=[COMPANY_SETTING_TAG],
    summary="Consulter les paramètres du restaurant",
    description=(
        "Retourne les paramètres publics de présentation du restaurant. "
        "Ces informations comprennent notamment le nom du restaurant, "
        "le logo, l'image de la barre de navigation, le slogan, "
        "les coordonnées et les informations des réseaux sociaux."
    ),
    responses={
        200: OpenApiResponse(
            description=(
                "Paramètres du restaurant retournés avec succès."
            )
        ),
    },
)