from django.urls import path
from .views.admin_category_views import AdminCategoryListView, AdminCategoryUpdateView, AdminCategoryDeleteView
from .views.admin_meal_views import AdminMealListView, AdminMealUpdateView, AdminMealDeleteView
from .views.admin_accompaniment_views import AdminAccompanimentListView, AdminAccompanimentUpdateView, AdminAccompanimentDeleteView
from .views.admin_boisson_views import AdminBoissonListView, AdminBoissonUpdateView, AdminBoissonDeleteView

app_name = "meal"

urlpatterns = [
    path("admin-dashboard/categories/", AdminCategoryListView.as_view(), name="category-list"),
    path("admin-dashboard/categories/<uuid:pk>/update/", AdminCategoryUpdateView.as_view(), name="category-update"),
    path("admin-dashboard/categories/<uuid:pk>/delete/", AdminCategoryDeleteView.as_view(), name="category-delete"),
    
    path("admin-dashboard/meals/", AdminMealListView.as_view(), name="meal-list"),
    path("admin-dashboard/meals/<uuid:pk>/update/", AdminMealUpdateView.as_view(), name="meal-update"),
    path("admin-dashboard/meals/<uuid:pk>/delete/", AdminMealDeleteView.as_view(), name="meal-delete"),
    
    path("admin-dashboard/accompaniments/", AdminAccompanimentListView.as_view(), name="accompaniment-list"),
    path("admin-dashboard/accompaniments/<uuid:pk>/update/", AdminAccompanimentUpdateView.as_view(), name="accompaniment-update"),
    path("admin-dashboard/accompaniments/<uuid:pk>/delete/", AdminAccompanimentDeleteView.as_view(), name="accompaniment-delete"),

    path("admin-dashboard/boissons/", AdminBoissonListView.as_view(), name="boisson-list"),
    path("admin-dashboard/boissons/<uuid:pk>/update/", AdminBoissonUpdateView.as_view(), name="boisson-update"),
    path("admin-dashboard/boissons/<uuid:pk>/delete/", AdminBoissonDeleteView.as_view(), name="boisson-delete"),
]
