from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect

from restaurants.meal.models import Category
from restaurants.meal.forms import CategoryForm


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class AdminCategoryListView(AdminRequiredMixin, ListView):
    model = Category
    template_name = "pages/dashboard/admin_dashboard/category_list.html"
    context_object_name = "categories"
    ordering = ["display_order", "name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = CategoryForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Catégorie créée avec succès !")
            return redirect("meal:category-list")
        
        messages.error(request, "Erreur lors de la création de la catégorie. Veuillez vérifier les champs.")
        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(form=form, show_modal=True))


class AdminCategoryUpdateView(AdminRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "pages/dashboard/admin_dashboard/category_update.html"
    success_url = reverse_lazy("meal:category-list")

    def form_valid(self, form):
        messages.success(self.request, "Catégorie mise à jour avec succès !")
        return super().form_valid(form)


class AdminCategoryDeleteView(AdminRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy("meal:category-list")

    def form_valid(self, form):
        messages.success(self.request, "Catégorie supprimée avec succès !")
        return super().form_valid(form)
