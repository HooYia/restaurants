from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from restaurants.users.models import Address


def _get_client(request):
    """Retourne le profil client ou None."""
    try:
        return request.user.client_profile
    except Exception:
        return None


class AddressListView(LoginRequiredMixin, View):
    template_name = "pages/dashboard/user_dashboad/addresses.html"

    def get(self, request):
        client = _get_client(request)
        if not client:
            messages.error(request, "Profil client introuvable.")
            return redirect("users:client-dashboard")

        addresses = client.addresses.filter(is_deleted=False).order_by("-is_default", "-created")
        return render(request, self.template_name, {
            "addresses": addresses,
            "active_page": "addresses",
        })


class AddressCreateView(LoginRequiredMixin, View):
    template_name = "pages/dashboard/user_dashboad/address_form.html"

    def get(self, request):
        return render(request, self.template_name, {"action": "Ajouter", "address": None})

    def post(self, request):
        client = _get_client(request)
        if not client:
            messages.error(request, "Profil client introuvable.")
            return redirect("users:client-dashboard")

        city = request.POST.get("city", "").strip()
        street = request.POST.get("street", "").strip()
        description = request.POST.get("description", "").strip()
        complement = request.POST.get("complement", "").strip()
        is_default = request.POST.get("is_default") == "on"

        if not city or not street:
            messages.error(request, "La ville et la rue sont obligatoires.")
            return render(request, self.template_name, {
                "action": "Ajouter",
                "address": None,
                "form_data": request.POST,
            })

        Address.objects.create(
            client=client,
            city=city,
            street=street,
            description=description,
            complement=complement,
            is_default=is_default,
        )
        messages.success(request, "Adresse ajoutée avec succès.")
        return redirect("users:address-list")


class AddressUpdateView(LoginRequiredMixin, View):
    template_name = "pages/dashboard/user_dashboad/address_form.html"

    def _get_address(self, request, pk):
        client = _get_client(request)
        if not client:
            return None, None
        return client, get_object_or_404(Address, pk=pk, client=client, is_deleted=False)

    def get(self, request, pk):
        client, address = self._get_address(request, pk)
        if not client:
            messages.error(request, "Profil client introuvable.")
            return redirect("users:client-dashboard")
        return render(request, self.template_name, {"action": "Modifier", "address": address})

    def post(self, request, pk):
        client, address = self._get_address(request, pk)
        if not client:
            messages.error(request, "Profil client introuvable.")
            return redirect("users:client-dashboard")

        city = request.POST.get("city", "").strip()
        street = request.POST.get("street", "").strip()

        if not city or not street:
            messages.error(request, "La ville et la rue sont obligatoires.")
            return render(request, self.template_name, {
                "action": "Modifier",
                "address": address,
                "form_data": request.POST,
            })

        address.city = city
        address.street = street
        address.description = request.POST.get("description", "").strip()
        address.complement = request.POST.get("complement", "").strip()
        address.is_default = request.POST.get("is_default") == "on"
        address.save()

        messages.success(request, "Adresse mise à jour.")
        return redirect("users:address-list")


class AddressDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        client = _get_client(request)
        if not client:
            messages.error(request, "Profil client introuvable.")
            return redirect("users:client-dashboard")

        address = get_object_or_404(Address, pk=pk, client=client, is_deleted=False)
        address.soft_delete()
        messages.success(request, "Adresse supprimée.")
        return redirect("users:address-list")


class AddressSetDefaultView(LoginRequiredMixin, View):

    def post(self, request, pk):
        client = _get_client(request)
        if not client:
            return redirect("users:client-dashboard")

        address = get_object_or_404(Address, pk=pk, client=client, is_deleted=False)
        address.is_default = True
        address.save()  # le signal dans Address.save() désactive les autres
        messages.success(request, f"« {address.street}, {address.city} » définie comme adresse par défaut.")
        return redirect("users:address-list")
