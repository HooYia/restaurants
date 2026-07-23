from django.urls import path
from .views.admin_category_views import AdminCategoryListView
from .views.admin_meal_views import AdminMealListView

app_name = "meal"

urlpatterns = [
    path("admin-dashboard/categories/", AdminCategoryListView.as_view(), name="category-list"),
    path("admin-dashboard/meals/", AdminMealListView.as_view(), name="meal-list"),
]
