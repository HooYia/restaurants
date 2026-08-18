from rest_framework import serializers

from restaurants.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }
