from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


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
            stats["loyalty_points"] = stats["total_orders"] * 10
            stats["total_testimonials"] = client.testimonials.count()

        popular_meals = Meal.objects.filter(is_available=True)[:3]

        return render(request, self.template_name, {
            "client_orders": client_orders,
            "stats": stats,
            "popular_meals": popular_meals,
        })


class AdminDashboardView(
    LoginRequiredMixin,
    TemplateView
):

    template_name = "pages/dashboard/admin_dashboard/admin_dashboard.html"