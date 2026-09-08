"""
Documentation Swagger de l'API de messagerie.
"""

from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers

from ..serializers.mobile_serializers import ErrorResponseSerializer


CHAT_TAG = "Chat / Messagerie"

MessageSchema = inline_serializer(
    name="ChatMessage",
    fields={
        "id": serializers.UUIDField(read_only=True),
        "sender_name": serializers.CharField(read_only=True),
        "sender_role": serializers.ChoiceField(choices=["client", "admin"], read_only=True),
        "order": serializers.UUIDField(allow_null=True, read_only=True),
        "content": serializers.CharField(),
        "attachment_url": serializers.URLField(allow_blank=True, read_only=True),
        "is_read": serializers.BooleanField(read_only=True),
        "read_at": serializers.DateTimeField(allow_null=True, read_only=True),
        "created": serializers.DateTimeField(read_only=True),
    },
)
ConversationSchema = inline_serializer(
    name="ClientConversation",
    fields={
        "id": serializers.UUIDField(read_only=True),
        "last_message_at": serializers.DateTimeField(allow_null=True, read_only=True),
        "messages": serializers.ListField(child=serializers.DictField(), read_only=True),
    },
)
AdminConversationSchema = inline_serializer(
    name="AdminConversation",
    fields={
        "id": serializers.UUIDField(read_only=True),
        "client_name": serializers.CharField(read_only=True),
        "client_email": serializers.EmailField(read_only=True),
        "last_message_at": serializers.DateTimeField(allow_null=True, read_only=True),
        "messages": serializers.ListField(child=serializers.DictField(), read_only=True),
    },
)
MessageCreateSchema = inline_serializer(
    name="ChatMessageCreate",
    fields={
        "content": serializers.CharField(required=False, allow_blank=True),
        "attachment": serializers.FileField(required=False, allow_null=True),
        "order_id": serializers.UUIDField(required=False, allow_null=True),
    },
)
AdminConversationListSchema = serializers.ListSerializer(
    child=inline_serializer(
        name="AdminConversationListItem",
        fields={
            "id": serializers.UUIDField(read_only=True),
            "client_name": serializers.CharField(read_only=True),
            "client_email": serializers.EmailField(read_only=True),
            "last_message_at": serializers.DateTimeField(allow_null=True, read_only=True),
            "unread_count": serializers.IntegerField(read_only=True),
        },
    ),
)


client_chat_get_doc = extend_schema(
    tags=[CHAT_TAG],
    summary="Consulter la conversation du client",
    description=(
        "Retourne la conversation entre le client authentifié et le support. "
        "Les messages non lus reçus du support sont automatiquement marqués "
        "comme lus lors de la consultation."
    ),
    responses={
        200: OpenApiResponse(response=ConversationSchema, description="Conversation et messages retournés."),
        401: OpenApiResponse(response=ErrorResponseSerializer, description="Authentification requise."),
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
    request=MessageCreateSchema,
    responses={
        201: OpenApiResponse(
            response=MessageSchema,
            description="Message envoyé avec succès."
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description=(
                "Le contenu ou la pièce jointe est requis, "
                "ou la commande associée est invalide."
            )
        ),
        401: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Authentification requise.",
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
            response=AdminConversationListSchema,
            description=(
                "Liste des conversations avec le nom du client, "
                "son email, la date du dernier message et le nombre "
                "de messages non lus."
            )
        ),
        401: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Authentification requise.",
        ),
        403: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Accès réservé aux administrateurs.",
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
            response=AdminConversationSchema,
            description=(
                "Conversation retournée avec les informations "
                "du client et les messages."
            )
        ),
        401: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Authentification requise.",
        ),
        403: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Accès réservé aux administrateurs.",
        ),
        404: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Conversation introuvable.",
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
    request=MessageCreateSchema,
    responses={
        201: OpenApiResponse(
            response=MessageSchema,
            description="Message envoyé avec succès."
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description=(
                "Le contenu ou la pièce jointe est requis."
            )
        ),
        401: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Authentification requise.",
        ),
        403: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Accès réservé aux administrateurs.",
        ),
        404: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Conversation introuvable.",
        ),
    },
)