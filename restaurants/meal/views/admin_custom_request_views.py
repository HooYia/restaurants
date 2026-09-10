from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .admin_order_views import AdminRequiredMixin
from restaurants.meal.models import CustomOrderRequest, Meal, Category
from restaurants.meal.enum import CustomRequestStatus

class AdminCustomRequestListView(AdminRequiredMixin, View):
    template_name = "pages/dashboard/admin_dashboard/custom_request_list.html"

    def get(self, request):
        status_filter = request.GET.get("status", "")
        requests = CustomOrderRequest.objects.select_related("client__user").order_by("-created")

        if status_filter and status_filter in dict(CustomRequestStatus.choices):
            requests = requests.filter(status=status_filter)

        status_choices_with_counts = [
            (s.value, s.label, CustomOrderRequest.objects.filter(status=s).count())
            for s in CustomRequestStatus
        ]
        
        return render(request, self.template_name, {
            "requests": requests,
            "status_filter": status_filter,
            "status_choices": CustomRequestStatus.choices,
            "status_choices_with_counts": status_choices_with_counts,
            "total": CustomOrderRequest.objects.count(),
            "active_page": "custom_requests",
        })

class AdminCustomRequestPriceView(AdminRequiredMixin, View):
    def post(self, request, pk):
        custom_req = get_object_or_404(CustomOrderRequest, pk=pk)
        action = request.POST.get("action")
        
        if action == "reject":
            custom_req.status = CustomRequestStatus.REJECTED
            custom_req.rejection_reason = request.POST.get("rejection_reason", "Refusé par l'administration.")
            custom_req.save()
            messages.success(request, "La demande a été refusée.")
        
        elif action == "price":
            price = request.POST.get("price")
            try:
                price_val = float(price)
                custom_req.proposed_price = price_val
                custom_req.status = CustomRequestStatus.PRICED
                
                # Create the hidden Meal
                cat, _ = Category.objects.get_or_create(name="Sur Mesure", defaults={'display_order': 999})
                meal_name = f"Plat sur mesure #{str(custom_req.id)[:8].upper()} ({custom_req.client.user.first_name})"
                meal = Meal.objects.create(
                    name=meal_name,
                    description=custom_req.description,
                    price=price_val,
                    category=cat,
                    is_available=False # Hidden from public menu
                )
                custom_req.linked_meal = meal
                custom_req.save()
                messages.success(request, f"Le tarif de {price_val} FCFA a été proposé.")
            except ValueError:
                messages.error(request, "Prix invalide.")
                
        return redirect("meal:admin-custom-request-list")
