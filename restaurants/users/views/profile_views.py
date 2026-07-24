from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from restaurants.users.forms import UserProfileUpdateForm
from restaurants.users.models import User


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileUpdateForm
    template_name = "pages/dashboard/user_dashboad/profile.html"
    success_url = reverse_lazy("users:profile-update")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Vos informations ont été mises à jour avec succès.")
        return super().form_valid(form)


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "pages/dashboard/user_dashboad/password_change.html"
    success_url = reverse_lazy("users:profile-update")

    def form_valid(self, form):
        messages.success(self.request, "Votre mot de passe a été modifié avec succès.")
        return super().form_valid(form)
