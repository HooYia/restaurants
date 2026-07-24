from django.urls import path
from restaurants.users.views.auth_views import CustomLogoutView

from restaurants.users.views.auth_views import RegisterView, VerifyOtpView
from restaurants.users.views.home_view import HomeView
from restaurants.users.views.cart_view import CartView
from restaurants.users.views.cart_api import CartAddView, CartRemoveView, CartUpdateView

from .views.login_views import LoginChoiceView, LoginView, ClientDashboardView, AdminDashboardView
app_name = "users"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "panier/",
        CartView.as_view(),
        name="cart"
    ),
    path(
        "api/cart/add/",
        CartAddView.as_view(),
        name="cart-add"
    ),
    path(
        "api/cart/remove/",
        CartRemoveView.as_view(),
        name="cart-remove"
    ),
    path(
        "api/cart/update/",
        CartUpdateView.as_view(),
        name="cart-update"
    ),
      path(
        "register/",
        RegisterView.as_view(),
        name="register"
    ),

       path(
        "verify-otp/",
        VerifyOtpView.as_view(),
        name="verify-otp",
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login"
    ),

     path(
        "login/",
        LoginChoiceView.as_view(),
        name="login"
    ),


    path(
        "client/dashboard/",
        ClientDashboardView.as_view(),
        name="client-dashboard"
    ),


path(
    "admin-dashboard/",
    AdminDashboardView.as_view(),
    name="admin-dashboard"
),
path(
    "logout/",
    CustomLogoutView.as_view(),
    name="logout"
)
]
