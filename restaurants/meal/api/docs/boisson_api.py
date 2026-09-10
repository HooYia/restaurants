"""Swagger du endpoint public ``views/boisson_api.py``."""

from drf_spectacular.utils import OpenApiResponse, extend_schema

from ..serializers.serializers import BoissonSerializer

boisson_list_doc = extend_schema(
    tags=["Menu public"],
    summary="Lister les boissons disponibles",
    description="Retourne uniquement les boissons disponibles à la commande.",
    responses={
        200: OpenApiResponse(
            description="Liste des boissons disponibles.",
            response=BoissonSerializer(many=True),
        ),
        500: OpenApiResponse(description="Erreur interne lors de la lecture des boissons."),
    },
)
