from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Client, Admin, Conversation

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create conversation for everyone
        Conversation.objects.create(user=instance)
        
        # Create specific profile
        if getattr(instance, 'is_staff', False) or getattr(instance, 'is_superuser', False):
            Admin.objects.get_or_create(user=instance)
        else:
            Client.objects.get_or_create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if getattr(instance, 'is_staff', False) or getattr(instance, 'is_superuser', False):
        Admin.objects.get_or_create(user=instance)
    else:
        Client.objects.get_or_create(user=instance)
