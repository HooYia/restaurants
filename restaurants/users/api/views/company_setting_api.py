"""Endpoint public des paramètres de présentation du restaurant."""

from rest_framework import permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurants.users.models import CompanySetting
from ..docs.company_setting import company_setting_get_doc


class CompanySettingSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    navbar_image_url = serializers.SerializerMethodField()

    class Meta:
        model = CompanySetting
        fields = (
            "restaurant_name", "logo_url", "navbar_image_url", "slogan", "address",
            "phone", "email", "facebook_url", "instagram_url", "whatsapp_url",
            "monday_friday", "saturday", "sunday", "copyright_text", "footer_note",
        )

    def _absolute_image_url(self, image):
        if not image:
            return ""
        request = self.context.get("request")
        return request.build_absolute_uri(image.url) if request else image.url

    def get_logo_url(self, obj):
        return self._absolute_image_url(obj.logo)

    def get_navbar_image_url(self, obj):
        return self._absolute_image_url(obj.navbar_image)


class CompanySettingAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CompanySettingSerializer

    @company_setting_get_doc
    def get(self, request):
        setting = CompanySetting.objects.first()
        if not setting:
            return Response({})
        return Response(self.serializer_class(setting, context={"request": request}).data)
