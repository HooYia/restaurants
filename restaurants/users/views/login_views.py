from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from restaurants.users.models import (
    HeroSection,
)


User = get_user_model()



class LoginChoiceView(View):

    template_name = "users/login_choice.html"


    def get(self, request):

        return render(
            request,
            self.template_name
        )



class LoginView(View):

    template_name = "users/login.html"


    def get(self, request):

        return render(
            request,
            self.template_name
        )


    def post(self, request):

        email = request.POST.get(
            "email"
        ).lower().strip()


        password = request.POST.get(
            "password"
        )


        user = authenticate(
            request,
            email=email,
            password=password
        )


        if user is None:

            messages.error(
                request,
                "Email ou mot de passe incorrect."
            )

            return redirect(
                "users:login"
            )


        login(
            request,
            user
        )

        messages.success(request, "Connexion réussie ! Heureux de vous revoir.")

        # ADMIN

        if user.is_staff or user.is_superuser:

            return redirect(
                "users:admin-dashboard"
            )


        # CLIENT

        if hasattr(user, "client_profile"):

            return redirect(
                "users:client-dashboard"
            )


        messages.error(
            request,
            "Votre compte n'a aucun profil associé."
        )


        return redirect(
            "users:login"
        )




class ClientDashboardView(LoginRequiredMixin, View):

    template_name = "pages/dashboard/user_dashboad/client_dashboard.html"

    def get(self, request):
        from restaurants.meal.models import Order, Meal

        try:
            client = request.user.client_profile
        except Exception:
            client = None

        client_orders = []
        stats = {
            "total_orders": 0,
            "loyalty_points": 0,
            "upcoming_reservations": 0,
            "total_testimonials": 0,
        }

        if client:
            client_orders = Order.objects.filter(client=client).prefetch_related("items")[:10]
            stats["total_orders"] = Order.objects.filter(client=client).count()
            stats["loyalty_points"] = client.loyalty_points
            stats["points_to_gift"] = max(100 - client.loyalty_points, 0)
            stats["total_testimonials"] = client.testimonials.count()

        popular_meals = Meal.objects.filter(is_available=True)[:3]

        return render(request, self.template_name, {
            "client_orders": client_orders,
            "stats": stats,
            "popular_meals": popular_meals,
        })


class AdminDashboardView(LoginRequiredMixin, View):

    template_name = "pages/dashboard/admin_dashboard/admin_dashboard.html"

    def get(self, request):
        from restaurants.meal.models import Order
        from restaurants.meal.enum import OrderStatus
        from restaurants.users.models import Client, Testimonial
        from django.utils import timezone
        from django.db.models import Sum

        today = timezone.now().date()

        

        # Stats
        today_orders = Order.objects.filter(created__date=today).count()
        pending_orders = Order.objects.filter(status=OrderStatus.PENDING).count()
        monthly_revenue = Order.objects.filter(
            status=OrderStatus.DELIVERED,
            created__year=today.year,
            created__month=today.month,
        ).aggregate(total=Sum("total_amount"))["total"] or 0
        new_clients = Client.objects.filter(created__date=today).count()

        from restaurants.users.models import Testimonial
        from restaurants.users.enum import TestimonialStatus
        pending_testimonials_qs = Testimonial.objects.filter(
            status=TestimonialStatus.PENDING
        ).select_related("client__user")[:5]
        pending_testimonials_count = Testimonial.objects.filter(
            status=TestimonialStatus.PENDING
        ).count()



        recent_orders = Order.objects.select_related(
            "client__user"
        ).prefetch_related("items").order_by("-created")[:8]

        stats = {
            "today_orders": today_orders,
            "pending_orders_count": pending_orders,
            "monthly_revenue": f"{int(monthly_revenue):,}".replace(",", " "),
            "new_clients": new_clients,
            "pending_testimonials_count": pending_testimonials_count,
        }

        return render(request, self.template_name, {
            "stats": stats,
            "recent_orders": recent_orders,
            "pending_testimonials": pending_testimonials_qs,
        })
    


    def get_context_data(
        self,
        **kwargs
    ):
        

        context = super().get_context_data(
            **kwargs
        )


        context["hero"] = (
            HeroSection.objects.first()
        )