from django.urls import path
from restaurants.users.views.auth_views import CustomLogoutView

from restaurants.users.views.auth_views import RegisterView, VerifyOtpView
from restaurants.users.views.home_view import HomeView
from restaurants.users.views.cart_view import CartView
from restaurants.users.views.cart_api import CartAddView, CartRemoveView, CartUpdateView
from restaurants.users.views.checkout_views import CheckoutView, OrderSuccessView

from .views.login_views import LoginChoiceView, LoginView, ClientDashboardView, AdminDashboardView
from .views.order_tracking_view import OrderTrackingView
from .views.address_views import (
    AddressListView, AddressCreateView, AddressUpdateView,
    AddressDeleteView, AddressSetDefaultView,
)
from .views.order_views import OrderListView
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
        "checkout/",
        CheckoutView.as_view(),
        name="checkout"
    ),
    path(
        "checkout/success/<uuid:order_id>/",
        OrderSuccessView.as_view(),
        name="order-success"
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
        "client/commandes/",
        OrderListView.as_view(),
        name="order-list"
    ),
    path(
        "client/commandes/<uuid:order_id>/suivi/",
        OrderTrackingView.as_view(),
        name="order-tracking"
    ),
    # Adresses
    path(
        "client/adresses/",
        AddressListView.as_view(),
        name="address-list"
    ),
    path(
        "client/adresses/ajouter/",
        AddressCreateView.as_view(),
        name="address-create"
    ),
    path(
        "client/adresses/<uuid:pk>/modifier/",
        AddressUpdateView.as_view(),
        name="address-update"
    ),
    path(
        "client/adresses/<uuid:pk>/supprimer/",
        AddressDeleteView.as_view(),
        name="address-delete"
    ),
    path(
        "client/adresses/<uuid:pk>/par-defaut/",
        AddressSetDefaultView.as_view(),
        name="address-set-default"
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
