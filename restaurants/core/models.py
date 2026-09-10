import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from model_utils.models import TimeStampedModel


class OngManager(models.Manager):
    """Manager par défaut qui exclut les objets supprimés logiquement."""
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class OngBaseModel(TimeStampedModel):
    """
    Modèle de base pour toute la plateforme :
    - UUID primary key
    - created / modified (TimeStampedModel)
    - is_active
    - soft delete
    - metadata JSON
    """

    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        unique=True,
        help_text=_("Identifiant UUID unique."),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_("Indique si l'objet est actif."),
    )
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        help_text=_("Suppression logique (soft delete)."),
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Métadonnées additionnelles au format JSON."),
    )

    objects = OngManager()
    all_objects = models.Manager()  # inclut les soft-deleted

    class Meta:
        abstract = True

    def soft_delete(self, save=True):  # noqa: FBT002
        self.is_deleted = True
        if save:
            self.save(update_fields=["is_deleted", "modified"])

    def restore(self, save=True):  # noqa: FBT002
        self.is_deleted = False
        if save:
            self.save(update_fields=["is_deleted", "modified"])

    def __str__(self):
        return str(self.id)


def _generate_unique_slug(instance, source_value):
    """Génère un slug unique, en tenant compte des objets supprimés logiquement."""
    base_slug = slugify(source_value) if source_value else str(instance.id)[:8]
    if not base_slug:
        base_slug = str(instance.id)[:8]

    model = instance.__class__
    slug = base_slug
    counter = 1
    
    # On utilise all_objects si disponible pour ne pas réutiliser le slug d'un objet supprimé
    manager = getattr(model, 'all_objects', model.objects)
    
    qs = manager.filter(slug=slug)
    if instance.pk:
        qs = qs.exclude(pk=instance.pk)

    while qs.exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
        qs = manager.filter(slug=slug)
        if instance.pk:
            qs = qs.exclude(pk=instance.pk)

    return slug
