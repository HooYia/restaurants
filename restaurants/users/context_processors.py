from django.conf import settings


def allauth_settings(request):
    """Expose some settings from django-allauth in templates."""
    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
    }

from restaurants.users.cart import Cart
def cart_processor(request):
    return {'cart': Cart(request)}

def dashboard_stats(request):
    # Seulement pour les pages de l'admin
    if '/admin-dashboard/' in request.path and getattr(request.user, 'is_authenticated', False) and (request.user.is_staff or request.user.is_superuser):
        try:
            from restaurants.meal.models import Order
            from restaurants.meal.enum import OrderStatus
            from restaurants.users.models import Testimonial
            from restaurants.users.enum import TestimonialStatus
            
            return {
                'sidebar_stats': {
                    'pending_orders_count': Order.objects.filter(status=OrderStatus.PENDING).count(),
                    'pending_testimonials_count': Testimonial.objects.filter(status=TestimonialStatus.PENDING).count(),
                }
            }
        except Exception:
            return {}
    return {}
