from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from restaurants.users.models import CompanySetting


class CompanySettingView(
    LoginRequiredMixin,
    UpdateView
):

    model = CompanySetting

    template_name = (
        "pages/dashboard/admin_dashboard/company_setting.html"
    )

    fields = [
        "restaurant_name",
        "logo",
        "navbar_image",
        "slogan",
        "address",
        "phone",
        "email",
        "facebook_url",
        "instagram_url",
        "whatsapp_url",
        "monday_friday",
        "saturday",
        "sunday",
        "copyright_text",
        "footer_note",
    ]

    def get_object(self):

        setting = CompanySetting.objects.first()

        if not setting:

            setting = CompanySetting.objects.create()

        return setting

    def form_valid(self, form):

        messages.success(
            self.request,
            "Paramètres mis à jour avec succès."
        )

        return super().form_valid(form)

    def get_success_url(self):

        return self.request.path