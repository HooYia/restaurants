from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import View

from restaurants.meal.models import Order
from restaurants.meal.enum import OrderStatus


# Ordre des statuts pour la timeline
STATUS_STEPS = [
    OrderStatus.PENDING,
    OrderStatus.CONFIRMED,
    OrderStatus.PREPARING,
    OrderStatus.READY,
    OrderStatus.DELIVERED,
]


class OrderTrackingView(LoginRequiredMixin, View):

    template_name = "pages/dashboard/user_dashboad/order_tracking.html"

    def get(self, request, order_id):
        try:
            client = request.user.client
        except Exception:
            from django.contrib import messages
            messages.error(request, "Accès non autorisé.")
            return __import__('django.shortcuts', fromlist=['redirect']).redirect('users:home')

        order = get_object_or_404(
            Order.objects.prefetch_related("items__meal", "items__accompaniments", "items__boisson"),
            id=order_id,
            client=client,
        )

        # Construire la timeline
        is_cancelled = order.status == OrderStatus.CANCELLED
        steps = []
        current_index = STATUS_STEPS.index(order.status) if order.status in STATUS_STEPS else -1

        for i, step in enumerate(STATUS_STEPS):
            if is_cancelled:
                state = "cancelled" if i == 0 else "inactive"
            elif i < current_index:
                state = "done"
            elif i == current_index:
                state = "active"
            else:
                state = "inactive"
            steps.append({"status": step, "label": dict(OrderStatus.choices)[step], "state": state})

        if is_cancelled:
            steps[0]["state"] = "done"
            steps.append({
                "status": OrderStatus.CANCELLED,
                "label": "Annulée",
                "state": "cancelled",
            })

        return render(request, self.template_name, {
            "order": order,
            "steps": steps,
            "is_cancelled": is_cancelled,
        })
