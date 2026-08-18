from django.urls import include, path

app_name = "api"

urlpatterns = [
    path(
        "v1/",
        include(
            ("restaurants.users.api.urls", "users_api"),
            namespace="users_api_v1",
        ),
    ),

    path(
        "v1/",
        include(
            ("restaurants.meal.api.urls", "meal_api"),
            namespace="meal_api_v1",
        ),
    ),
]