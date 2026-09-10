from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

from restaurants.meal.models import Accompaniment
from restaurants.meal.forms import AccompanimentForm
from restaurants.meal.views.admin_category_views import AdminRequiredMixin


class AdminAccompanimentListView(AdminRequiredMixin, ListView):
    model = Accompaniment
    template_name = "pages/dashboard/admin_dashboard/accompaniment_list.html"
    context_object_name = "accompaniments"
    ordering = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = AccompanimentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = AccompanimentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Accompagnement créé avec succès !")
            return redirect("meal:accompaniment-list")
        
        messages.error(request, "Erreur lors de la création de l'accompagnement. Veuillez vérifier les champs.")
        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(form=form, show_modal=True))


class AdminAccompanimentUpdateView(AdminRequiredMixin, UpdateView):
    model = Accompaniment
    form_class = AccompanimentForm
    template_name = "pages/dashboard/admin_dashboard/accompaniment_update.html"
    success_url = reverse_lazy("meal:accompaniment-list")

    def form_valid(self, form):
        messages.success(self.request, "Accompagnement mis à jour avec succès !")
        return super().form_valid(form)


class AdminAccompanimentDeleteView(AdminRequiredMixin, DeleteView):
    model = Accompaniment
    success_url = reverse_lazy("meal:accompaniment-list")

    def form_valid(self, form):
        messages.success(self.request, "Accompagnement supprimé avec succès !")
        return super().form_valid(form)
