"""
Documentation Swagger de l'API Newsletter.
"""

from drf_spectacular.utils import extend_schema, OpenApiResponse

from ..serializers.mobile_serializers import ErrorResponseSerializer, NewsletterSerializer


NEWSLETTER_TAG = "Newsletter"


newsletter_create_doc = extend_schema(
    tags=[NEWSLETTER_TAG],
    summary="S'inscrire à la newsletter",
    description=(
        "Permet à un visiteur de s'inscrire à la newsletter du restaurant. "
        "L'inscription est publique et ne nécessite pas d'authentification."
    ),
    request=NewsletterSerializer,
    responses={
        201: OpenApiResponse(
            response=NewsletterSerializer,
            description=(
                "Inscription à la newsletter effectuée avec succès."
            )
        ),
        200: OpenApiResponse(
            description=(
                "L'adresse existait précédemment mais avait été supprimée. "
                "L'abonnement a été restauré."
            ),
            response=NewsletterSerializer,
        ),
        400: OpenApiResponse(
            description=(
                "L'adresse email est invalide ou est déjà abonnée "
                "à la newsletter."
            ),
            response=ErrorResponseSerializer,
        ),
    },
)