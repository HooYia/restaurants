from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from restaurants.meal.models import Order
from restaurants.meal.enum import OrderStatus


class OrderListView(LoginRequiredMixin, View):
    template_name = "pages/dashboard/user_dashboad/orders.html"

    def get(self, request):
        try:
            client = request.user.client_profile
        except Exception:
            from django.contrib import messages
            messages.error(request, "Profil client introuvable.")
            return redirect("users:client-dashboard")

        status_filter = request.GET.get("status", "")

        orders = Order.objects.filter(client=client).prefetch_related("items__meal")

        if status_filter and status_filter in dict(OrderStatus.choices):
            orders = orders.filter(status=status_filter)

        orders = orders.order_by("-created")

        # Compteurs par statut pour les badges
        counts = {}
        for s in OrderStatus:
            counts[s] = Order.objects.filter(client=client, status=s).count()

        return render(request, self.template_name, {
            "orders": orders,
            "status_filter": status_filter,
            "status_choices": OrderStatus.choices,
            "counts": counts,
            "active_page": "orders",
        })
