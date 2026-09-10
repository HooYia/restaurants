"""API de messagerie entre un client et les administrateurs."""

from django.utils import timezone
from rest_framework import permissions, serializers, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurants.meal.models import Order
from restaurants.users.models import Conversation, Message
from ..docs.chat import (
    admin_chat_detail_doc, admin_chat_list_doc, admin_chat_message_doc,
    client_chat_get_doc, client_chat_post_doc,
)


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.name", read_only=True)
    sender_role = serializers.SerializerMethodField()
    attachment_url = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id", "sender_name", "sender_role", "order", "content", "attachment_url",
            "is_read", "read_at", "created",
        )

    def get_sender_role(self, obj):
        return "admin" if obj.sender.is_staff else "client"

    def get_attachment_url(self, obj):
        if not obj.attachment:
            return ""
        request = self.context.get("request")
        return request.build_absolute_uri(obj.attachment.url) if request else obj.attachment.url


class MessageCreateSerializer(serializers.Serializer):
    content = serializers.CharField(required=False, allow_blank=True)
    attachment = serializers.FileField(required=False, allow_null=True)
    order_id = serializers.UUIDField(required=False, allow_null=True)

    def validate(self, attrs):
        if not attrs.get("content", "").strip() and not attrs.get("attachment"):
            raise serializers.ValidationError("Le contenu ou une pièce jointe est requis.")
        return attrs


def serialize_conversation(conversation, request):
    messages = conversation.messages.select_related("sender").order_by("created")
    return {
        "id": str(conversation.id),
        "last_message_at": conversation.last_message_at,
        "messages": MessageSerializer(messages, many=True, context={"request": request}).data,
    }


class ClientChatAPIView(APIView):
    """Conversation de l'utilisateur connecté avec le support."""

    serializer_class = MessageCreateSerializer

    def get_conversation(self, user):
        conversation, _ = Conversation.objects.get_or_create(user=user)
        return conversation

    @client_chat_get_doc
    def get(self, request):
        conversation = self.get_conversation(request.user)
        conversation.messages.filter(is_read=False).exclude(sender=request.user).update(
            is_read=True, read_at=timezone.now()
        )
        return Response(serialize_conversation(conversation, request))

    @client_chat_post_doc
    def post(self, request):
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = self.get_conversation(request.user)
        order = None
        order_id = serializer.validated_data.get("order_id")
        if order_id:
            if not hasattr(request.user, "client_profile"):
                raise ValidationError({"order_id": "Seul un client peut associer une commande."})
            try:
                order = Order.objects.get(id=order_id, client=request.user.client_profile)
            except Order.DoesNotExist as exc:
                raise ValidationError({"order_id": "Commande introuvable."}) from exc
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            order=order,
            content=serializer.validated_data.get("content", "").strip(),
            attachment=serializer.validated_data.get("attachment"),
        )
        return Response(MessageSerializer(message, context={"request": request}).data, status=status.HTTP_201_CREATED)


class AdminChatListAPIView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    @admin_chat_list_doc
    def get(self, request):
        conversations = Conversation.objects.select_related("user").order_by("-last_message_at")
        data = [
            {
                "id": str(conversation.id),
                "client_name": conversation.user.name,
                "client_email": conversation.user.email,
                "last_message_at": conversation.last_message_at,
                "unread_count": conversation.messages.filter(is_read=False, sender__is_staff=False).count(),
            }
            for conversation in conversations
        ]
        return Response(data)


class AdminChatDetailAPIView(APIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = MessageCreateSerializer

    def get_conversation(self, conversation_id):
        try:
            return Conversation.objects.select_related("user").get(id=conversation_id)
        except Conversation.DoesNotExist as exc:
            raise NotFound("Conversation introuvable.") from exc

    @admin_chat_detail_doc
    def get(self, request, conversation_id):
        conversation = self.get_conversation(conversation_id)
        conversation.messages.filter(is_read=False, sender__is_staff=False).update(
            is_read=True, read_at=timezone.now()
        )
        data = serialize_conversation(conversation, request)
        data["client_name"] = conversation.user.name
        data["client_email"] = conversation.user.email
        return Response(data)


class AdminChatMessageAPIView(AdminChatDetailAPIView):
    @admin_chat_message_doc
    def post(self, request, conversation_id):
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = self.get_conversation(conversation_id)
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=serializer.validated_data.get("content", "").strip(),
            attachment=serializer.validated_data.get("attachment"),
        )
        return Response(MessageSerializer(message, context={"request": request}).data, status=status.HTTP_201_CREATED)
