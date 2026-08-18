"""
Documentation Swagger de l'API des adresses client.
"""

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)


ADDRESS_TAG = "Adresses"


address_list_doc = extend_schema(
    tags=[ADDRESS_TAG],
    summary="Lister les adresses",
    description=(
        "Retourne la liste des adresses appartenant "
        "au client authentifié."
    ),
)


address_create_doc = extend_schema(
    tags=[ADDRESS_TAG],
    summary="Créer une adresse",
    description=(
        "Crée une nouvelle adresse pour le client "
        "authentifié."
    ),
)


address_detail_doc = extend_schema(
    tags=[ADDRESS_TAG],
    summary="Consulter une adresse",
    description=(
        "Retourne les informations d'une adresse "
        "du client authentifié."
    ),
)


address_update_doc = extend_schema(
    tags=[ADDRESS_TAG],
    summary="Modifier une adresse",
    description=(
        "Modifie complètement une adresse existante."
    ),
)


address_partial_update_doc = extend_schema(
    tags=[ADDRESS_TAG],
    summary="Modifier partiellement une adresse",
    description=(
        "Modifie partiellement une adresse existante."
    ),
)


address_delete_doc = extend_schema(
    tags=[ADDRESS_TAG],
    summary="Supprimer une adresse",
    description=(
        "Supprime logiquement une adresse existante."
    ),
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
            description="Adresse définie comme adresse par défaut."
        ),
    },
)
