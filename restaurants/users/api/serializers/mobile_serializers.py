from rest_framework import serializers

from restaurants.meal.models import Boisson, Category, CustomOrderRequest, Meal, Order, OrderItem
from restaurants.users.models import Address, NewsletterSubscriber, Testimonial, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone", "name"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id", "street", "city", "description", "complement",
            "gps_lat", "gps_lng", "is_default",
        ]


class RegisterOtpSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)


class VerifyOtpSerializer(serializers.Serializer):
    verification_id = serializers.UUIDField()
    otp = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"].lower()
        password = attrs["password"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as exc:
            raise serializers.ValidationError({"email": ["Identifiants invalides."]}) from exc

        if not user.check_password(password):
            raise serializers.ValidationError({"email": ["Identifiants invalides."]})

        attrs["user"] = user
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class BoissonSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Boisson
        fields = ["id", "name", "slug", "price", "image_url", "is_available"]

    def get_image_url(self, obj) -> str:
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
            "id", "name", "slug", "description", "price", "image_url", "category",
            "is_available", "max_included_accompaniments", "accompaniments",
        ]

    def get_image_url(self, obj) -> str:
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else ""


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "meal", "quantity", "unit_price", "subtotal"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "status", "total_amount", "created", "items"]


class OrderCreateSerializer(serializers.Serializer):
    delivery_address_id = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, attrs):
        return attrs


class CustomOrderRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomOrderRequest
        fields = ["id", "description", "quantity", "target_date", "status", "created"]


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ["id", "rating", "comment", "status", "created"]
        read_only_fields = ["id", "status", "created"]


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ["id", "email"]
