from datetime import date

from django.core.cache import cache
from django.db.models import Exists, OuterRef
from django.views.generic import TemplateView

from restaurants.meal.enum import DayOfWeek
from restaurants.meal.models import Boisson, Category, DailyMenu, Meal
from restaurants.users.enum import TestimonialStatus
from restaurants.users.models import HeroSection, Testimonial


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today_day = date.today().strftime('%A').lower()
        selected_day = self.request.GET.get('day', '').strip().lower()

        if selected_day not in {value for value, _ in DayOfWeek.choices}:
            selected_day = ''

        meals_queryset = Meal.objects.filter(is_available=True).select_related('category').prefetch_related('daily_menus')

        if selected_day:
            meals_queryset = meals_queryset.filter(daily_menus__day=selected_day, daily_menus__is_active=True).distinct()

        meals = list(
            meals_queryset.annotate(
                is_today=Exists(
                    DailyMenu.objects.filter(
                        day=today_day,
                        is_active=True,
                        meals=OuterRef('pk')
                    )
                )
            ).order_by('-is_today', 'category__display_order', 'name')
        )

        categories = cache.get('home_categories')
        if categories is None:
            categories = list(Category.objects.order_by('display_order').all())
            cache.set('home_categories', categories, 86400)

        daily_menus = cache.get('home_daily_menus')
        if daily_menus is None:
            daily_menus = list(DailyMenu.objects.filter(is_active=True).order_by('day'))
            cache.set('home_daily_menus', daily_menus, 86400)

        context['meals'] = meals
        context['boissons'] = list(Boisson.objects.filter(is_available=True))
        context['categories'] = categories
        context['daily_menus'] = daily_menus
        context['selected_day'] = selected_day
        context['days'] = [{'value': value, 'label': label} for value, label in DayOfWeek.choices]
        context['testimonials'] = Testimonial.objects.filter(status=TestimonialStatus.APPROVED)[:5]
        context['hero'] = HeroSection.objects.first()
        return context