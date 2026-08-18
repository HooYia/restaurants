"""
Documentation Swagger de l'API des avis client.
"""

from drf_spectacular.utils import extend_schema, OpenApiResponse


TESTIMONIAL_TAG = "Avis client"


testimonial_get_doc = extend_schema(
    tags=[TESTIMONIAL_TAG],
    summary="Consulter son avis",
    description=(
        "Retourne l'avis du client authentifié. "
        "Si le client n'a pas encore soumis d'avis, une réponse vide "
        "est retournée."
    ),
    responses={
        200: OpenApiResponse(
            description=(
                "Avis du client retourné avec succès, "
                "ou réponse vide si aucun avis n'existe."
            )
        ),
        401: OpenApiResponse(
            description="Authentification requise."
        ),
    },
)


testimonial_update_doc = extend_schema(
    tags=[TESTIMONIAL_TAG],
    summary="Créer ou modifier son avis",
    description=(
        "Permet au client authentifié de créer ou modifier son avis. "
        "L'avis est automatiquement associé au client connecté et "
        "son statut est défini à PENDING après l'enregistrement."
    ),
    responses={
        200: OpenApiResponse(
            description="Avis créé ou modifié avec succès."
        ),
        400: OpenApiResponse(
            description="Données de l'avis invalides."
        ),
        401: OpenApiResponse(
            description="Authentification requise."
        ),
    },
)