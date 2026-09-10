"""
Documentation Swagger de l'API panier.
"""

from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema

from ..serializers.mobile_serializers import (
    CartAddSerializer,
    CartBoissonSerializer,
    CartComponentUpdateSerializer,
    CartItemRemoveSerializer,
    CartItemUpdateSerializer,
    CartResponseSerializer,
)


CART_TAG = "Panier"


cart_detail_doc = extend_schema(
    tags=[CART_TAG],
    summary="Consulter le panier",
    description=(
        "Retourne le contenu du panier de session avec la liste des articles, "
        "le nombre total d'articles et le montant total du panier."
    ),
    responses={
        200: OpenApiResponse(
            description="Contenu du panier retourné avec succès.",
            response=CartResponseSerializer,
        ),
    },
)


cart_add_doc = extend_schema(
    tags=[CART_TAG],
    summary="Ajouter un plat au panier",
    description=(
        "Ajoute un plat disponible au panier. "
        "Le plat peut être accompagné d'accompagnements et de boissons."
    ),
    request=CartAddSerializer,
    responses={
        200: OpenApiResponse(
            description="Plat ajouté au panier avec succès.",
            response=CartResponseSerializer,
        ),
        400: OpenApiResponse(
            description=(
                "Quantité invalide ou accompagnement/boisson invalide."
            ),
        ),
        404: OpenApiResponse(
            description="Plat introuvable ou indisponible."
        ),
    },
)


cart_remove_doc = extend_schema(
    tags=[CART_TAG],
    summary="Supprimer un article du panier",
    description=(
        "Supprime un article du panier à partir de son identifiant."
    ),
    request=CartItemRemoveSerializer,
    responses={
        200: OpenApiResponse(
            description="Article supprimé du panier avec succès.",
            response=CartResponseSerializer,
        ),
    },
)


cart_update_doc = extend_schema(
    tags=[CART_TAG],
    summary="Modifier la quantité d'un article",
    description=(
        "Modifie la quantité d'un article déjà présent dans le panier."
    ),
    request=CartItemUpdateSerializer,
    responses={
        200: OpenApiResponse(
            description="Quantité mise à jour avec succès.",
            response=CartResponseSerializer,
        ),
    },
)


cart_update_component_doc = extend_schema(
    tags=[CART_TAG],
    summary="Modifier un composant d'un article",
    description=(
        "Modifie la quantité d'un accompagnement ou d'une boisson "
        "associée à un article du panier."
    ),
    request=CartComponentUpdateSerializer,
    responses={
        200: OpenApiResponse(
            description="Composant mis à jour avec succès.",
            response=CartResponseSerializer,
        ),
        400: OpenApiResponse(
            description="Type de composant invalide."
        ),
    },
)


cart_add_boisson_doc = extend_schema(
    tags=[CART_TAG],
    summary="Ajouter une boisson au panier",
    description=(
        "Ajoute une boisson disponible directement au panier."
    ),
    request=CartBoissonSerializer,
    responses={
        200: OpenApiResponse(
            description="Boisson ajoutée au panier avec succès.",
            response=CartResponseSerializer,
        ),
        400: OpenApiResponse(
            description="La quantité doit être supérieure à zéro."
        ),
        404: OpenApiResponse(
            description="Boisson introuvable ou indisponible."
        ),
    },
)