from django.urls import path
from .views.admin_category_views import AdminCategoryListView

app_name = "meal"

urlpatterns = [
    path("admin-dashboard/categories/", AdminCategoryListView.as_view(), name="category-list"),
]
