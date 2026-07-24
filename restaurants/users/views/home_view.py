from django.views.generic import TemplateView
from restaurants.meal.models import Meal, Accompaniment, Boisson

class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meals'] = Meal.objects.filter(is_available=True).select_related('category')
        context['accompaniments'] = Accompaniment.objects.all()
        context['boissons'] = Boisson.objects.filter(is_available=True)
        return context