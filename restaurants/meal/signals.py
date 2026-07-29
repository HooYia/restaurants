from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.cache import cache
from .models import Meal, Boisson, Category, DailyMenu

def clear_home_cache():
    # Since today's day can be anything, we can't just clear a single key easily without knowing it, 
    # but we can clear all 7 possible days, or use cache.delete_many
    days = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    keys_to_delete = [f'home_meals_{day}' for day in days]
    keys_to_delete.extend(['home_boissons', 'home_categories', 'home_daily_menus'])
    cache.delete_many(keys_to_delete)

@receiver([post_save, post_delete], sender=Meal)
@receiver([post_save, post_delete], sender=Boisson)
@receiver([post_save, post_delete], sender=Category)
@receiver([post_save, post_delete], sender=DailyMenu)
def invalidate_home_cache(sender, instance, **kwargs):
    clear_home_cache()

@receiver(m2m_changed, sender=DailyMenu.meals.through)
def invalidate_home_cache_m2m(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        clear_home_cache()
