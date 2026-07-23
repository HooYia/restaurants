from django.views.generic import ListView
from django.contrib import messages
from django.shortcuts import redirect

from restaurants.meal.models import Meal
from restaurants.meal.forms import MealForm
from restaurants.meal.views.admin_category_views import AdminRequiredMixin


class AdminMealListView(AdminRequiredMixin, ListView):
    model = Meal
    template_name = "pages/dashboard/admin_dashboard/meal_list.html"
    context_object_name = "meals"
    ordering = ["category__display_order", "name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = MealForm()
        return context

    def post(self, request, *args, **kwargs):
        form = MealForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Plat créé avec succès !")
            return redirect("meal:meal-list")
        
        messages.error(request, "Erreur lors de la création du plat. Veuillez vérifier les champs.")
        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(form=form, show_modal=True))
