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
    email = serializers.EmailField(
        help_text="Adresse email utilisée lors de l'inscription.",
    )
    otp = serializers.CharField(
        min_length=6,
        max_length=6,
        help_text="Code OTP à 6 chiffres reçu par email.",
    )


class OtpSentSerializer(serializers.Serializer):
    detail = serializers.CharField()
    email = serializers.EmailField()


class TokenResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()


class ErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
    field = serializers.ListField(child=serializers.CharField(), required=False)


class CartComponentSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1, default=1)


class CartAddSerializer(serializers.Serializer):
    meal_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1, default=1)
    accompaniments = CartComponentSerializer(many=True, required=False)
    boissons = CartComponentSerializer(many=True, required=False)


class CartBoissonSerializer(serializers.Serializer):
    boisson_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1, default=1)


class CartItemUpdateSerializer(serializers.Serializer):
    item_id = serializers.CharField()
    quantity = serializers.IntegerField(min_value=0)


class CartItemRemoveSerializer(serializers.Serializer):
    item_id = serializers.CharField()


class CartComponentUpdateSerializer(serializers.Serializer):
    item_id = serializers.CharField()
    component_type = serializers.ChoiceField(choices=["accompaniment", "boisson"])
    component_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=0)


class CartItemSerializer(serializers.Serializer):
    id = serializers.CharField()
    quantity = serializers.IntegerField()
    meal_id = serializers.UUIDField(required=False)
    boisson_id = serializers.UUIDField(required=False)
    meal_name = serializers.CharField()
    meal_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    accompaniments = serializers.ListField()
    boissons = serializers.ListField()


class CartResponseSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    count = serializers.IntegerField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)


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
