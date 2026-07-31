from django.views.generic import TemplateView
from django.db.models import Exists, OuterRef
from django.core.cache import cache
import datetime
from restaurants.meal.models import Meal, Boisson, DailyMenu, Category
from restaurants.users.models import Testimonial

from restaurants.meal.models import Meal, Boisson, DailyMenu
from restaurants.users.models import Testimonial, HeroSection
from restaurants.users.enum import TestimonialStatus


class HomeView(TemplateView):

    template_name = "pages/home.html"


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)


        today_day = datetime.date.today().strftime('%A').lower()
        
        meals_cache_key = f'home_meals_{today_day}'
        meals = cache.get(meals_cache_key)
        if meals is None:
            meals = list(Meal.objects.filter(is_available=True).annotate(
                is_today=Exists(
                    DailyMenu.objects.filter(
                        day=today_day, 
                        is_active=True, 
                        meals=OuterRef('pk')
                    )
                )
            ).order_by('-is_today', 'category__display_order', 'name').select_related('category').prefetch_related('daily_menus'))
            cache.set(meals_cache_key, meals, 86400)
            
        boissons = cache.get('home_boissons')
        if boissons is None:
            boissons = list(Boisson.objects.filter(is_available=True))
            cache.set('home_boissons', boissons, 86400)
            
        categories = cache.get('home_categories')
        if categories is None:
            categories = list(Category.objects.all().order_by('display_order'))
            cache.set('home_categories', categories, 86400)
            
        daily_menus = cache.get('home_daily_menus')
        if daily_menus is None:
            daily_menus = list(DailyMenu.objects.filter(is_active=True))
            cache.set('home_daily_menus', daily_menus, 86400)
            
        context['meals'] = meals
        context['boissons'] = boissons
        context['categories'] = categories
        context['daily_menus'] = daily_menus
        context['testimonials'] = Testimonial.objects.filter(status=TestimonialStatus.APPROVED)[:5]


        # Menus disponibles
        context["meals"] = (
            Meal.objects
            .filter(is_available=True)
            .annotate(
                is_today=Exists(
                    DailyMenu.objects.filter(
                        day=today_day,
                        is_active=True,
                        meals=OuterRef("pk")
                    )
                )
            )
            .order_by(
                "-is_today",
                "category__display_order",
                "name"
            )
            .select_related("category")
        )


        # Boissons
        context["boissons"] = (
            Boisson.objects
            .filter(is_available=True)
        )


        # Témoignages validés
        context["testimonials"] = (
            Testimonial.objects
            .filter(
                status=TestimonialStatus.APPROVED
            )[:5]
        )


        # Section Hero modifiable par admin
        context["hero"] = (
            HeroSection.objects.first()
        )


        return context