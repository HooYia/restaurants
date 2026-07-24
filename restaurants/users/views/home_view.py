from django.views.generic import TemplateView
from django.db.models import Exists, OuterRef
import datetime
from restaurants.meal.models import Meal, Boisson, DailyMenu
from restaurants.users.models import Testimonial
from restaurants.users.enum import TestimonialStatus

class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        today_day = datetime.date.today().strftime('%A').lower()
        
        context['meals'] = Meal.objects.filter(is_available=True).annotate(
            is_today=Exists(
                DailyMenu.objects.filter(
                    day=today_day, 
                    is_active=True, 
                    meals=OuterRef('pk')
                )
            )
        ).order_by('-is_today', 'category__display_order', 'name').select_related('category')
        
        context['boissons'] = Boisson.objects.filter(is_available=True)
        context['testimonials'] = Testimonial.objects.filter(status=TestimonialStatus.APPROVED)[:5]
        return context