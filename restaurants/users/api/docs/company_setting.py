"""
Documentation Swagger de l'API des paramètres de présentation
du restaurant.
"""

from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers


COMPANY_SETTING_TAG = "Paramètres du restaurant"

CompanySettingSchema = inline_serializer(
    name="CompanySetting",
    fields={
        "restaurant_name": serializers.CharField(),
        "logo_url": serializers.URLField(allow_blank=True),
        "navbar_image_url": serializers.URLField(allow_blank=True),
        "slogan": serializers.CharField(allow_blank=True),
        "address": serializers.CharField(allow_blank=True),
        "phone": serializers.CharField(allow_blank=True),
        "email": serializers.EmailField(allow_blank=True),
        "facebook_url": serializers.URLField(allow_blank=True),
        "instagram_url": serializers.URLField(allow_blank=True),
        "whatsapp_url": serializers.URLField(allow_blank=True),
        "monday_friday": serializers.CharField(allow_blank=True),
        "saturday": serializers.CharField(allow_blank=True),
        "sunday": serializers.CharField(allow_blank=True),
        "copyright_text": serializers.CharField(allow_blank=True),
        "footer_note": serializers.CharField(allow_blank=True),
    },
)


company_setting_get_doc = extend_schema(
    tags=[COMPANY_SETTING_TAG],
    summary="Consulter les paramètres du restaurant",
    description=(
        "Retourne les paramètres publics de présentation du restaurant. "
        "Ces informations comprennent notamment le nom du restaurant, "
        "le logo, l'image de la barre de navigation, le slogan, "
        "les coordonnées et les informations des réseaux sociaux."
    ),
    responses={
        200: OpenApiResponse(
            response=CompanySettingSchema,
            description=(
                "Paramètres du restaurant retournés avec succès."
            )
        ),
    },
)