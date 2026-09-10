"""Swagger du endpoint public ``views/category_api.py``."""

from drf_spectacular.utils import OpenApiResponse, extend_schema

from ..serializers.serializers import CategorySerializer

category_list_doc = extend_schema(
    tags=["Menu public"],
    summary="Lister les catégories",
    description="Retourne les catégories du menu, dans leur ordre d'affichage.",
    responses={
        200: OpenApiResponse(
            description="Liste des catégories du menu.",
            response=CategorySerializer(many=True),
        ),
        500: OpenApiResponse(description="Erreur interne lors de la lecture des catégories."),
    },
)
