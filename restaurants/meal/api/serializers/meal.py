from rest_framework import serializers

from restaurants.meal.models import Boisson, Meal

from .category import CategorySerializer


class BoissonSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Boisson
        fields = ["id", "name", "slug", "price", "image_url", "is_available"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else ""


class MealSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    accompaniments = serializers.StringRelatedField(many=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Meal
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "image_url",
            "category",
            "is_available",
            "max_included_accompaniments",
            "accompaniments",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else ""
