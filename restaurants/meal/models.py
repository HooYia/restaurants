import uuid

from django.db import models
from django.utils.text import slugify

from .enum import AvailabilityMode, DayOfWeek, OrderStatus, PaymentMethod, PaymentStatus
from restaurants.users.models import Address, Client
from restaurants.core.models import OngBaseModel



class Category(OngBaseModel):
    """Catégorie de plat : Plats principaux, Accompagnements, Boissons..."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name[:1].upper() + self.name[1:]
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Accompaniment(OngBaseModel):
    """
    Accompagnement proposable pour un plat (ex : plantain frit,
    bâton de manioc). Un même accompagnement peut être rattaché
    à plusieurs plats via Meal.accompaniments.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "Accompagnement"
        verbose_name_plural = "Accompagnements"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name[:1].upper() + self.name[1:]
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Boisson(OngBaseModel):
    """Boisson proposable en supplément d'une commande."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="boissons/", blank=True, null=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Boisson"
        verbose_name_plural = "Boissons"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name[:1].upper() + self.name[1:]
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Meal(OngBaseModel):
    """
    Plat du menu. L'admin définit ici la liste des accompagnements
    proposables (accompaniments) et le nombre inclus gratuitement
    (max_included_accompaniments) — tout choix du client au-delà
    de ce nombre est facturé en supplément sur l'OrderItem.
    """
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="meals/", blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="meals"
    )
    accompaniments = models.ManyToManyField(
        Accompaniment,
        blank=True,
        related_name="meals",
        help_text="Accompagnements proposables pour ce plat",
    )
    max_included_accompaniments = models.PositiveSmallIntegerField(
        default=0,
        help_text="Nombre d'accompagnements inclus gratuitement dans le prix du plat",
    )
    availability_mode = models.CharField(
        max_length=20,
        choices=AvailabilityMode.choices,
        default=AvailabilityMode.ALWAYS,
    )
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Plat"
        verbose_name_plural = "Plats"
        ordering = ["category__display_order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name[:1].upper() + self.name[1:]
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class DailyMenu(OngBaseModel):
    """
    Menu journalier (Lundi, Mardi, etc.).
    Permet de regrouper les plats (Meals) disponibles ce jour-là.
    """
    day = models.CharField(
        max_length=15, 
        choices=DayOfWeek.choices, 
        unique=True,
        help_text="Jour de la semaine"
    )
    meals = models.ManyToManyField(
        Meal,
        blank=True,
        related_name="daily_menus",
        help_text="Plats disponibles ce jour-là"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Désactiver ce jour rendra indisponible tout son menu."
    )

    class Meta:
        verbose_name = "Menu Journalier"
        verbose_name_plural = "Menus Journaliers"

    def __str__(self):
        return f"Menu du {self.get_day_display()}"


class Order(OngBaseModel):
    """Commande passée par un client."""
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="orders"
    )
    delivery_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    payment_method = models.CharField(
        max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ["-created"]

    def __str__(self):
        return f"Commande {self.id} — {self.client}"

    def recalculate_total(self, save=True):
        """Recalcule total_amount à partir de la somme des OrderItem.subtotal."""
        total = sum((item.subtotal for item in self.items.all()), start=0)
        self.total_amount = total
        if save:
            self.save(update_fields=["total_amount"])
        return total


class OrderItem(OngBaseModel):
    """
    Ligne de commande : un plat, sa quantité, les accompagnements
    choisis par le client (parmi ceux définis sur le Meal) et une
    boisson optionnelle. Le supplément dû aux accompagnements en
    trop est stocké dans extra_accompaniments_fee.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    meal = models.ForeignKey(
        Meal, on_delete=models.PROTECT, related_name="order_items", null=True, blank=True
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Prix du plat au moment de la commande (indépendant d'un futur changement de prix)",
    )
    accompaniments = models.ManyToManyField(
        Accompaniment,
        through='OrderItemAccompaniment',
        blank=True,
        related_name="order_items",
        help_text="Accompagnements choisis par le client avec leur quantité",
    )
    boissons = models.ManyToManyField(
        Boisson,
        through='OrderItemBoisson',
        blank=True,
        related_name="order_items",
        help_text="Boissons choisies par le client avec leur quantité",
    )
    extra_accompaniments_fee = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"

    def __str__(self):
        return f"{self.quantity} x {self.meal}"

    def recalculate(self, save=True):
        """
        À appeler après avoir défini les accompagnements (M2M) et les
        boissons : calcule le supplément d'accompagnements et le
        sous-total de la ligne.
        """
        # Collect chosen accompaniments expanded by their quantity
        chosen = []
        for oia in self.order_item_accompaniments.select_related('accompaniment').all():
            for _ in range(oia.quantity):
                chosen.append(oia.accompaniment)
        
        # Sort by price to give the cheapest ones for free
        chosen.sort(key=lambda a: a.price)
        
        included = self.meal.max_included_accompaniments if self.meal else 0
        extra = chosen[included:]
        self.extra_accompaniments_fee = sum(
            (a.price for a in extra), start=0
        )

        boisson_price = sum(
            (oib.boisson.price * oib.quantity for oib in self.order_item_boissons.select_related('boisson').all()),
            start=0
        )
        self.subtotal = (
            self.unit_price * self.quantity
            + self.extra_accompaniments_fee
            + boisson_price
        )
        if save:
            self.save(update_fields=["extra_accompaniments_fee", "subtotal"])
        return self.subtotal

class OrderItemAccompaniment(OngBaseModel):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='order_item_accompaniments')
    accompaniment = models.ForeignKey(Accompaniment, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Accompagnement de commande"
        verbose_name_plural = "Accompagnements de commande"
        unique_together = ('order_item', 'accompaniment')

    def __str__(self):
        return f"{self.quantity} x {self.accompaniment.name}"

class OrderItemBoisson(OngBaseModel):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='order_item_boissons')
    boisson = models.ForeignKey(Boisson, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Boisson de commande"
        verbose_name_plural = "Boissons de commande"
        unique_together = ('order_item', 'boisson')

    def __str__(self):
        return f"{self.quantity} x {self.boisson.name}"


class Payment(OngBaseModel):
    """Paiement lié 1-1 à une commande."""
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payment"
    )
    method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"

    def __str__(self):
        return f"Paiement {self.get_status_display()} — {self.order}"