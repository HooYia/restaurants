from django.views.generic import DeleteView, DetailView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.core.files.uploadedfile import UploadedFile

from restaurants.meal.enum import AvailabilityMode, DayOfWeek
from restaurants.meal.models import Accompaniment, Category, DailyMenu, Meal
from restaurants.meal.views.admin_category_views import AdminRequiredMixin


def ensure_daily_menus():
    for value, _ in DayOfWeek.choices:
        DailyMenu.objects.get_or_create(day=value, defaults={"is_active": True})
    return DailyMenu.objects.filter(is_active=True).order_by("day")


class AdminMealListView(AdminRequiredMixin, ListView):
    model = Meal
    template_name = "pages/dashboard/admin_dashboard/meal_list.html"
    context_object_name = "meals"
    ordering = ["category__display_order", "name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.order_by("display_order", "name")
        context["accompaniments"] = Accompaniment.objects.order_by("name")
        context["daily_menus"] = ensure_daily_menus()
        context["available_modes"] = AvailabilityMode.choices
        return context

    def post(self, request, *args, **kwargs):
        name = (request.POST.get("name") or "").strip()
        description = (request.POST.get("description") or "").strip()
        category_id = request.POST.get("category")
        price_raw = (request.POST.get("price") or "0").replace(",", ".").strip()
        availability_mode = request.POST.get("availability_mode") or AvailabilityMode.ALWAYS
        is_available = request.POST.get("is_available") == "on"

        if not name or not category_id or not price_raw:
            messages.error(request, "Le nom, la catégorie et le prix sont obligatoires.")
            self.object_list = self.get_queryset()
            return self.render_to_response(self.get_context_data(show_modal=True))

        meal = Meal(
            name=name,
            description=description,
            price=price_raw,
            category_id=category_id,
            max_included_accompaniments=int(request.POST.get("max_included_accompaniments") or 0),
            availability_mode=availability_mode,
            is_available=is_available,
        )

        uploaded_image = request.FILES.get("image")
        if isinstance(uploaded_image, UploadedFile):
            meal.image = uploaded_image

        meal.save()
        accompaniments = request.POST.getlist("accompaniments")
        if accompaniments:
            meal.accompaniments.set(Accompaniment.objects.filter(pk__in=accompaniments))
        else:
            meal.accompaniments.clear()

        daily_ids = request.POST.getlist("daily_menus")
        if daily_ids:
            meal.daily_menus.set(DailyMenu.objects.filter(pk__in=daily_ids))
        else:
            meal.daily_menus.clear()

        messages.success(request, "Plat créé avec succès !")
        return redirect("meal:meal-list")


class AdminMealUpdateView(AdminRequiredMixin, DetailView):
    model = Meal
    template_name = "pages/dashboard/admin_dashboard/meal_update.html"
    context_object_name = "meal"
    success_url = reverse_lazy("meal:meal-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meal = self.object
        context["categories"] = Category.objects.order_by("display_order", "name")
        context["accompaniments"] = Accompaniment.objects.order_by("name")
        context["daily_menus"] = ensure_daily_menus()
        context["selected_accompaniment_ids"] = list(meal.accompaniments.values_list("id", flat=True))
        context["selected_daily_menu_ids"] = list(meal.daily_menus.values_list("id", flat=True))
        context["available_modes"] = AvailabilityMode.choices
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = (request.POST.get("name") or "").strip()
        description = (request.POST.get("description") or "").strip()
        category_id = request.POST.get("category")
        price_raw = (request.POST.get("price") or "0").replace(",", ".").strip()
        availability_mode = request.POST.get("availability_mode") or AvailabilityMode.ALWAYS
        is_available = request.POST.get("is_available") == "on"

        if not name or not category_id or not price_raw:
            messages.error(request, "Le nom, la catégorie et le prix sont obligatoires.")
            return self.render_to_response(self.get_context_data())

        self.object.name = name
        self.object.description = description
        self.object.category_id = category_id
        self.object.price = price_raw
        self.object.max_included_accompaniments = int(request.POST.get("max_included_accompaniments") or 0)
        self.object.availability_mode = availability_mode
        self.object.is_available = is_available

        uploaded_image = request.FILES.get("image")
        if isinstance(uploaded_image, UploadedFile):
            self.object.image = uploaded_image

        self.object.save()
        accompaniments = request.POST.getlist("accompaniments")
        if accompaniments:
            self.object.accompaniments.set(Accompaniment.objects.filter(pk__in=accompaniments))
        else:
            self.object.accompaniments.clear()

        daily_ids = request.POST.getlist("daily_menus")
        if daily_ids:
            self.object.daily_menus.set(DailyMenu.objects.filter(pk__in=daily_ids))
        else:
            self.object.daily_menus.clear()

        messages.success(request, "Plat mis à jour avec succès !")
        return redirect(self.success_url)


class AdminMealDeleteView(AdminRequiredMixin, DeleteView):
    model = Meal
    success_url = reverse_lazy("meal:meal-list")

    def form_valid(self, form):
        messages.success(self.request, "Plat supprimé avec succès !")
        return super().form_valid(form)
