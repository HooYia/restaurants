from django.db import models


class TestimonialStatus(models.TextChoices):
    """Statut de modération d'un avis client."""
    PENDING = "pending", "En attente"
    APPROVED = "approved", "Approuvé"
    REJECTED = "rejected", "Rejeté"