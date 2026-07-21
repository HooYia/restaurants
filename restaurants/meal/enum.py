from django.db import models


class AvailabilityMode(models.TextChoices):
    """Mode de disponibilité d'un plat."""
    ALWAYS = "always", "Toujours disponible"
    SPECIFIC_DAYS = "specific_days", "Jours spécifiques"
    SOLD_OUT = "sold_out", "Épuisé"


class OrderStatus(models.TextChoices):
    """Statut d'avancement d'une commande."""
    PENDING = "pending", "En attente"
    CONFIRMED = "confirmed", "Confirmée"
    PREPARING = "preparing", "En préparation"
    READY = "ready", "Prête"
    DELIVERED = "delivered", "Livrée"
    CANCELLED = "cancelled", "Annulée"


class PaymentMethod(models.TextChoices):
    """Moyen de paiement d'une commande."""
    CASH = "cash", "Espèces"
    MOBILE_MONEY = "mobile_money", "Mobile Money"
    CARD = "card", "Carte bancaire"


class PaymentStatus(models.TextChoices):
    """Statut du paiement lié à une commande."""
    PENDING = "pending", "En attente"
    PAID = "paid", "Payé"
    FAILED = "failed", "Échoué"
    REFUNDED = "refunded", "Remboursé"