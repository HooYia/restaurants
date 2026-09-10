from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.views.generic import ListView

from restaurants.users.models import User


class AdminUserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Vue admin listant tous les utilisateurs."""
    model = User
    template_name = "pages/dashboard/admin_dashboard/admin_user_list.html"
    context_object_name = "users"
    paginate_by = 20

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_queryset(self):
        qs = super().get_queryset().order_by("-date_joined")
        
        # Recherche par nom ou email
        search_query = self.request.GET.get("q")
        if search_query:
            qs = qs.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )
            
        # Filtre par rôle
        role_filter = self.request.GET.get("role")
        if role_filter == "admin":
            qs = qs.filter(is_staff=True)
        elif role_filter == "client":
            qs = qs.filter(is_staff=False)
            
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        context["role_filter"] = self.request.GET.get("role", "")
        return context
