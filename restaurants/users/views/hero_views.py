# restaurants/users/views/hero_views.py

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from restaurants.users.models import HeroSection


class AdminHeroView(LoginRequiredMixin, View):

    template_name = "pages/dashboard/admin_dashboard/admin_hero.html"


    def get(self, request):

        hero, created = HeroSection.objects.get_or_create(
            id=1
        )

        return render(
            request,
            self.template_name,
            {
                "hero": hero
            }
        )


    def post(self, request):

        hero, created = HeroSection.objects.get_or_create(
            id=1
        )


        # Gestion des images
        if request.FILES.get("image_1"):
            hero.image_1 = request.FILES.get("image_1")


        if request.FILES.get("image_2"):
            hero.image_2 = request.FILES.get("image_2")


        if request.FILES.get("image_3"):
            hero.image_3 = request.FILES.get("image_3")


        if request.FILES.get("image_4"):
            hero.image_4 = request.FILES.get("image_4")


        # Si votre modèle possède des champs texte
        # décommentez selon vos champs
        
        if "title" in request.POST:
            hero.title = request.POST.get("title")


        if "subtitle" in request.POST:
            hero.subtitle = request.POST.get("subtitle")


        if "description" in request.POST:
            hero.description = request.POST.get("description")


        hero.save()


        messages.success(
            request,
            "La section Hero a été mise à jour avec succès."
        )


        return redirect(
            "users:admin-hero"
        )