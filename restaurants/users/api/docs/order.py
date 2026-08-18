"""
Documentation Swagger des API de commandes client.
"""

from drf_spectacular.utils import extend_schema, OpenApiResponse


ORDER_TAG = "Commandes"


order_list_doc = extend_schema(
    tags=[ORDER_TAG],
    summary="Lister les commandes du client",
    description=(
        "Retourne la liste des commandes appartenant au client authentifié. "
        "Les commandes sont accompagnées de leur adresse de livraison, "
        "des articles commandés, des catégories des plats, des "
        "accompagnements et des boissons associés."
    ),
    responses={
        200: OpenApiResponse(
            description="Liste des commandes du client retournée avec succès."
        ),
        401: OpenApiResponse(
            description="Authentification requise."
        ),
    },
)


order_detail_doc = extend_schema(
    tags=[ORDER_TAG],
    summary="Consulter une commande",
    description=(
        "Retourne le détail d'une commande appartenant au client "
        "authentifié, avec son adresse de livraison et ses articles."
    ),
    responses={
        200: OpenApiResponse(
            description="Détails de la commande retournés avec succès."
        ),
        401: OpenApiResponse(
            description="Authentification requise."
        ),
        404: OpenApiResponse(
            description="Commande introuvable."
        ),
    },
)


order_create_doc = extend_schema(
    tags=[ORDER_TAG],
    summary="Créer une commande",
    description=(
        "Crée une nouvelle commande à partir des données envoyées "
        "par le client authentifié. La commande créée est ensuite "
        "retournée avec ses informations détaillées."
    ),
    responses={
        201: OpenApiResponse(
            description="Commande créée avec succès."
        ),
        400: OpenApiResponse(
            description="Données de commande invalides."
        ),
        401: OpenApiResponse(
            description="Authentification requise."
        ),
    },
)


custom_order_request_list_doc = extend_schema(
    tags=[ORDER_TAG],
    summary="Lister les demandes de commande personnalisées",
    description=(
        "Retourne les demandes de commande personnalisées "
        "du client authentifié."
    ),
    responses={
        200: OpenApiResponse(
            description=(
                "Liste des demandes de commande personnalisées "
                "retournée avec succès."
            )
        ),
        401: OpenApiResponse(
            description="Authentification requise."
        ),
    },
)


custom_order_request_detail_doc = extend_schema(
    tags=[ORDER_TAG],
    summary="Consulter une demande de commande personnalisée",
    description=(
        "Retourne le détail d'une demande de commande personnalisée "
        "appartenant au client authentifié."
    ),
    responses={
        200: OpenApiResponse(
            description="Demande retournée avec succès."
        ),
        401: OpenApiResponse(
            description="Authentification requise."
        ),
        404: OpenApiResponse(
            description="Demande de commande introuvable."
        ),
    },
)


custom_order_request_create_doc = extend_schema(
    tags=[ORDER_TAG],
    summary="Créer une demande de commande personnalisée",
    description=(
        "Permet au client authentifié de créer une demande "
        "de commande personnalisée. Le client est automatiquement "
        "associé à la demande."
    ),
    responses={
        201: OpenApiResponse(
            description="Demande créée avec succès."
        ),
        400: OpenApiResponse(
            description="Données de demande invalides."
        ),
        401: OpenApiResponse(
            description="Authentification requise."
        ),
    },
)