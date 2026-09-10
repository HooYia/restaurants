from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

from restaurants.meal.models import Boisson
from restaurants.meal.forms import BoissonForm
from restaurants.meal.views.admin_category_views import AdminRequiredMixin


class AdminBoissonListView(AdminRequiredMixin, ListView):
    model = Boisson
    template_name = "pages/dashboard/admin_dashboard/boisson_list.html"
    context_object_name = "boissons"
    ordering = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = BoissonForm()
        return context

    def post(self, request, *args, **kwargs):
        form = BoissonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Boisson créée avec succès !")
            return redirect("meal:boisson-list")
        
        messages.error(request, "Erreur lors de la création de la boisson. Veuillez vérifier les champs.")
        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(form=form, show_modal=True))


class AdminBoissonUpdateView(AdminRequiredMixin, UpdateView):
    model = Boisson
    form_class = BoissonForm
    template_name = "pages/dashboard/admin_dashboard/boisson_update.html"
    success_url = reverse_lazy("meal:boisson-list")

    def form_valid(self, form):
        messages.success(self.request, "Boisson mise à jour avec succès !")
        return super().form_valid(form)


class AdminBoissonDeleteView(AdminRequiredMixin, DeleteView):
    model = Boisson
    success_url = reverse_lazy("meal:boisson-list")

    def form_valid(self, form):
        messages.success(self.request, "Boisson supprimée avec succès !")
        return super().form_valid(form)
