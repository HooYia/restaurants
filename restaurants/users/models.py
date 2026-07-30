import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.base_user import BaseUserManager

from .enum import TestimonialStatus
from restaurants.core.models import OngBaseModel


class UserManager(BaseUserManager):

    def create_user(
        self,
        email,
        password=None,
        phone=None,
        first_name="",
        last_name="",
        **extra_fields
    ):

        if not email:
            raise ValueError("L'adresse email est requise")

        if not phone:
            raise ValueError("Le numéro de téléphone est requis")

        if not password:
            raise ValueError("Le mot de passe est requis")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        email,
        password=None,
        **extra_fields
    ):

        extra_fields.setdefault(
            "is_staff",
            True
        )

        extra_fields.setdefault(
            "is_superuser",
            True
        )

        extra_fields.setdefault(
            "is_active",
            True
        )

        user = self.model(
            email=self.normalize_email(email),
            phone=None,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user


class User(AbstractUser):

    username = None

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Admin(OngBaseModel):
    """Profil administrateur, lié 1-1 à un User."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="admin_profile",
    )

    def __str__(self):
        return f"Admin: {self.user}"


class Client(OngBaseModel):
    """Profil client, lié 1-1 à un User."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_profile",
    )

    def __str__(self):
        return f"Client: {self.user}"


class Address(OngBaseModel):
    """
    Adresse d'un client. Un client peut avoir plusieurs adresses,
    une seule peut être marquée par défaut (is_default).
    """
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="addresses"
    )
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    description = models.CharField(
        max_length=255,
        blank=True,
        help_text="Ex : quartier, point de repère",
    )
    complement = models.CharField(
        max_length=255,
        blank=True,
        help_text="Ex : porte, étage, complément d'adresse",
    )
    gps_lat = models.FloatField(null=True, blank=True)
    gps_lng = models.FloatField(null=True, blank=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Adresse"
        verbose_name_plural = "Adresses"

    def __str__(self):
        return f"{self.street}, {self.city}"

    def save(self, *args, **kwargs):
        # Une seule adresse par défaut par client
        if self.is_default:
            Address.objects.filter(client=self.client, is_default=True).exclude(
                pk=self.pk
            ).update(is_default=False)
        super().save(*args, **kwargs)


class Conversation(OngBaseModel):
    """
    Une conversation unique par utilisateur, réutilisée pour tout
    échange lié à ses commandes (support / SAV).
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversation",
    )
    last_message_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Conversation de {self.user}"


class Message(OngBaseModel):
    """Message envoyé dans une conversation, par le client ou un admin."""
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )
    order = models.ForeignKey(
        'meal.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
        help_text="Commande concernée par ce message (optionnel)"
    )
    content = models.TextField(blank=True)
    attachment = models.FileField(upload_to="messages/attachments/", null=True, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"Message de {self.sender} — {self.created:%d/%m/%Y %H:%M}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Met à jour le timestamp du dernier message sur la conversation
        Conversation.objects.filter(pk=self.conversation_id).update(
            last_message_at=self.created
        )


class Testimonial(OngBaseModel):
    """Avis laissé par un client, modéré avant publication."""
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="testimonials"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=TestimonialStatus.choices,
        default=TestimonialStatus.PENDING,
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Avis de {self.client} ({self.rating}/5)"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.client}-{uuid.uuid4().hex[:6]}")
            self.slug = base_slug
        super().save(*args, **kwargs)


class NewsletterSubscriber(OngBaseModel):
    """Abonné à la newsletter."""
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Abonné Newsletter"
        verbose_name_plural = "Abonnés Newsletter"

    def __str__(self):
        return self.email