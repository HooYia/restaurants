from django.urls import path
from restaurants.users.views import (
    address_views,
    auth_views,
    login_views,
    order_views,
    profile_views,
    testimonial_views,
    admin_user_views,
)
from restaurants.users.views.hero_views import AdminHeroView
from restaurants.users.views.auth_views import CustomLogoutView
from restaurants.users.views.hero_views import AdminHeroView
from restaurants.users.views.auth_views import RegisterView, VerifyOtpView
from restaurants.users.views.home_view import HomeView
from restaurants.users.views.cart_view import CartView
from restaurants.users.views.cart_api import CartAddView, CartRemoveView, CartUpdateView, CartAddBoissonView, CartUpdateComponentView
from restaurants.users.views.checkout_views import CheckoutView, OrderSuccessView
from restaurants.users.views.company_setting_views import (
    CompanySettingView,
)
from .views.login_views import LoginChoiceView, LoginView, ClientDashboardView, AdminDashboardView
from .views.order_tracking_view import OrderTrackingView
from .views.admin_messages_view import AdminMessagesView
from .views.client_messages_view import ClientMessagesView
from .views.newsletter_view import NewsletterSubscribeView
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
        "api/cart/add-boisson/",
        CartAddBoissonView.as_view(),
        name="cart-add-boisson"
    ),
    path(
        "api/cart/update/",
        CartUpdateView.as_view(),
        name="cart-update"
    ),
    path(
        "api/cart/update-component/",
        CartUpdateComponentView.as_view(),
        name="cart-update-component"
    ),
    path(
        "api/newsletter/subscribe/",
        NewsletterSubscribeView.as_view(),
        name="newsletter-subscribe"
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

    # Profile
    path(
        "profil/",
        view=profile_views.ProfileUpdateView.as_view(),
        name="profile-update",
    ),
    path(
        "profil/mot-de-passe/",
        view=profile_views.UserPasswordChangeView.as_view(),
        name="password-change",
    ),
    path(
        "client/commandes/<uuid:order_id>/suivi/",
        OrderTrackingView.as_view(),
        name="order-tracking"
    ),
    path(
        "client/messages/",
        ClientMessagesView.as_view(),
        name="client-messages"
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

    # Avis Client
    path(
        "client/avis/rediger/",
        testimonial_views.ClientTestimonialCreateView.as_view(),
        name="testimonial-create"
    ),

    # Demandes sur mesure
    path(
        "client/sur-mesure/demander/",
        __import__('restaurants.users.views.client_custom_request_views', fromlist=['ClientCustomRequestCreateView']).ClientCustomRequestCreateView.as_view(),
        name="custom-request-create"
    ),
    path(
        "client/sur-mesure/",
        __import__('restaurants.users.views.client_custom_request_views', fromlist=['ClientCustomRequestListView']).ClientCustomRequestListView.as_view(),
        name="custom-request-list"
    ),

path(
    "admin-dashboard/",
    AdminDashboardView.as_view(),
    name="admin-dashboard"
),
path(
    "admin-dashboard/messages/",
    AdminMessagesView.as_view(),
    name="admin-messages"
),
path(
    "admin-dashboard/avis/",
    testimonial_views.AdminTestimonialListView.as_view(),
    name="admin-testimonial-list"
),
path(
    "admin-dashboard/avis/<uuid:pk>/statut/",
    testimonial_views.AdminTestimonialStatusUpdateView.as_view(),
    name="admin-testimonial-status"
),
path(
    "admin-dashboard/utilisateurs/",
    admin_user_views.AdminUserListView.as_view(),
    name="admin-user-list"
),
path(
    "logout/",
    CustomLogoutView.as_view(),
    name="logout"
),
 path(
        "admin-hero/",
        AdminHeroView.as_view(),
        name="admin-hero"
    ),

path(
    "company-settings/",
    CompanySettingView.as_view(),
    name="company-settings"
),    
]
