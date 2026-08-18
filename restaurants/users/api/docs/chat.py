"""
Documentation Swagger de l'API de messagerie.
"""

from drf_spectacular.utils import extend_schema, OpenApiResponse


CHAT_TAG = "Chat / Messagerie"


client_chat_get_doc = extend_schema(
    tags=[CHAT_TAG],
    summary="Consulter la conversation du client",
    description=(
        "Retourne la conversation entre le client authentifié et le support. "
        "Les messages non lus reçus du support sont automatiquement marqués "
        "comme lus lors de la consultation."
    ),
    responses={
        200: OpenApiResponse(
            description=(
                "Conversation retournée avec son identifiant, "
                "la date du dernier message et la liste des messages."
            )
        ),
        401: OpenApiResponse(
            description="Authentification requise."
        ),
    },
)


client_chat_post_doc = extend_schema(
    tags=[CHAT_TAG],
    summary="Envoyer un message au support",
    description=(
        "Permet au client authentifié d'envoyer un message au support. "
        "Le message peut contenir du texte, une pièce jointe ou être "
        "associé à une commande."
    ),
    responses={
        201: OpenApiResponse(
            description="Message envoyé avec succès."
        ),
        400: OpenApiResponse(
            description=(
                "Le contenu ou la pièce jointe est requis, "
                "ou la commande associée est invalide."
            )
        ),
        401: OpenApiResponse(
            description="Authentification requise."
        ),
    },
)


admin_chat_list_doc = extend_schema(
    tags=[CHAT_TAG],
    summary="Lister les conversations des clients",
    description=(
        "Retourne la liste des conversations disponibles pour les "
        "administrateurs. Les conversations sont classées de la plus "
        "récente à la plus ancienne."
    ),
    responses={
        200: OpenApiResponse(
            description=(
                "Liste des conversations avec le nom du client, "
                "son email, la date du dernier message et le nombre "
                "de messages non lus."
            )
        ),
        401: OpenApiResponse(
            description="Authentification requise."
        ),
        403: OpenApiResponse(
            description="Accès réservé aux administrateurs."
        ),
    },
)


admin_chat_detail_doc = extend_schema(
    tags=[CHAT_TAG],
    summary="Consulter une conversation client",
    description=(
        "Retourne le détail d'une conversation spécifique avec "
        "l'ensemble de ses messages. Les messages non lus du client "
        "sont automatiquement marqués comme lus."
    ),
    responses={
        200: OpenApiResponse(
            description=(
                "Conversation retournée avec les informations "
                "du client et les messages."
            )
        ),
        401: OpenApiResponse(
            description="Authentification requise."
        ),
        403: OpenApiResponse(
            description="Accès réservé aux administrateurs."
        ),
        404: OpenApiResponse(
            description="Conversation introuvable."
        ),
    },
)


admin_chat_message_doc = extend_schema(
    tags=[CHAT_TAG],
    summary="Répondre à un client",
    description=(
        "Permet à un administrateur d'envoyer un message dans "
        "une conversation existante avec un client. "
        "Le message peut contenir du texte et/ou une pièce jointe."
    ),
    responses={
        201: OpenApiResponse(
            description="Message envoyé avec succès."
        ),
        400: OpenApiResponse(
            description=(
                "Le contenu ou la pièce jointe est requis."
            )
        ),
        401: OpenApiResponse(
            description="Authentification requise."
        ),
        403: OpenApiResponse(
            description="Accès réservé aux administrateurs."
        ),
        404: OpenApiResponse(
            description="Conversation introuvable."
        ),
    },
)