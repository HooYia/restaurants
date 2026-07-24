from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View, UpdateView

from restaurants.users.forms import TestimonialForm
from restaurants.users.models import Testimonial
from restaurants.users.enum import TestimonialStatus


class ClientTestimonialCreateView(LoginRequiredMixin, UpdateView):
    """Vue pour permettre à un client de soumettre ou modifier son avis unique."""
    model = Testimonial
    form_class = TestimonialForm
    template_name = "pages/dashboard/user_dashboad/testimonial_create.html"
    success_url = reverse_lazy("users:client-dashboard")

    def get_object(self, queryset=None):
        if not hasattr(self.request.user, 'client_profile'):
            return None
        return Testimonial.objects.filter(client=self.request.user.client_profile).first()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if not hasattr(self.request.user, 'client_profile'):
            messages.error(self.request, "Vous devez avoir un profil client pour laisser un avis.")
            return redirect("users:home")
            
        form.instance.client = self.request.user.client_profile
        
        # S'il s'agit d'une modification ou d'une nouvelle création, on remet le statut à PENDING
        if form.has_changed() or not self.object:
            form.instance.status = TestimonialStatus.PENDING
            if self.object:
                messages.success(self.request, "Votre avis a été modifié avec succès. Il est de nouveau en attente de validation par l'équipe.")
            else:
                messages.success(self.request, "Merci ! Votre avis a été soumis et est en attente de validation.")
        else:
            messages.info(self.request, "Aucune modification n'a été apportée à votre avis.")
            
        return super().form_valid(form)


class AdminTestimonialListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Vue admin listant tous les témoignages."""
    model = Testimonial
    template_name = "pages/dashboard/admin_dashboard/admin_testimonial_list.html"
    context_object_name = "testimonials"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_queryset(self):
        qs = super().get_queryset().select_related("client__user")
        
        # Filtre optionnel par statut
        status = self.request.GET.get("status")
        if status in [s[0] for s in TestimonialStatus.choices]:
            qs = qs.filter(status=status)
            
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["TestimonialStatus"] = TestimonialStatus
        context["current_status"] = self.request.GET.get("status", "")
        return context


class AdminTestimonialStatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Vue admin pour approuver ou rejeter un avis."""
    
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def post(self, request, pk, *args, **kwargs):
        testimonial = get_object_or_404(Testimonial, pk=pk)
        action = request.POST.get("action")
        
        if action == "approve":
            testimonial.status = TestimonialStatus.APPROVED
            messages.success(request, f"L'avis de {testimonial.client.user.get_full_name()} a été approuvé.")
        elif action == "reject":
            testimonial.status = TestimonialStatus.REJECTED
            messages.success(request, f"L'avis de {testimonial.client.user.get_full_name()} a été rejeté.")
            
        testimonial.save()
        
        # Redirection vers l'URL de provenance ou la liste des avis
        next_url = request.POST.get("next")
        if next_url:
            return redirect(next_url)
        return redirect("users:admin-testimonial-list")
