from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone

from restaurants.meal.models import Order
from restaurants.meal.enum import OrderStatus


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class AdminOrderListView(AdminRequiredMixin, View):
    template_name = "pages/dashboard/admin_dashboard/order_list.html"

    def get(self, request):
        status_filter = request.GET.get("status", "")
        search = request.GET.get("q", "").strip()

        orders = Order.objects.select_related(
            "client__user", "delivery_address"
        ).prefetch_related("items__meal").order_by("-created")

        if status_filter and status_filter in dict(OrderStatus.choices):
            orders = orders.filter(status=status_filter)

        if search:
            orders = orders.filter(
                client__user__first_name__icontains=search
            ) | orders.filter(
                client__user__last_name__icontains=search
            ) | orders.filter(
                client__user__email__icontains=search
            )

        # Liste (value, label, count) pour les filtres
        status_choices_with_counts = [
            (s.value, s.label, Order.objects.filter(status=s).count())
            for s in OrderStatus
        ]
        total = Order.objects.count()

        return render(request, self.template_name, {
            "orders": orders,
            "status_filter": status_filter,
            "search": search,
            "status_choices": OrderStatus.choices,
            "status_choices_with_counts": status_choices_with_counts,
            "counts": {s.value: Order.objects.filter(status=s).count() for s in OrderStatus},
            "total": total,
            "active_page": "orders",
        })


class AdminOrderUpdateStatusView(AdminRequiredMixin, View):
    """Change le statut d'une commande via un POST (appelé depuis la liste ou détail)."""

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get("status", "")

        if new_status not in dict(OrderStatus.choices):
            messages.error(request, "Statut invalide.")
            return redirect("meal:order-list")

        if order.status == OrderStatus.CANCELLED:
            messages.warning(request, "Impossible de modifier une commande annulée.")
            return redirect("meal:order-list")

        old_label = order.get_status_display()
        order.status = new_status
        order.save(update_fields=["status"])

        # Send Email to Client via Celery
        try:
            from restaurants.users.tasks import send_order_status_update_task
            send_order_status_update_task.delay(order.id)
        except Exception as e:
            pass

        new_label = order.get_status_display()
        messages.success(
            request,
            f"Commande #{str(order.id)[:8].upper()} : {old_label} → {new_label}"
        )
        return redirect(f"{request.META.get('HTTP_REFERER', '/admin-dashboard/commandes/')}")
