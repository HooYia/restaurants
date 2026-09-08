"""Swagger du endpoint public ``views/meal_api.py``."""

from drf_spectacular.utils import OpenApiResponse, extend_schema

from ..serializers.serializers import MealSerializer

meal_list_doc = extend_schema(
    tags=["Menu public"],
    summary="Lister les plats disponibles",
    description="Retourne uniquement les plats actuellement disponibles à la commande.",
    responses={
        200: OpenApiResponse(
            description="Liste des plats disponibles.",
            response=MealSerializer(many=True),
        ),
        500: OpenApiResponse(description="Erreur interne lors de la lecture du menu."),
    },
)
meal_detail_doc = extend_schema(
    tags=["Menu public"],
    summary="Consulter un plat",
    description="Retourne le détail d'un plat disponible, avec sa catégorie et ses accompagnements.",
    responses={
        200: OpenApiResponse(description="Détail du plat.", response=MealSerializer),
        404: OpenApiResponse(description="Plat introuvable ou indisponible."),
        500: OpenApiResponse(description="Erreur interne lors de la lecture du plat."),
    },
)
