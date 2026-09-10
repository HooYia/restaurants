from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views.address_api import AddressViewSet
from .views.auth_api import (
    LoginAPIView,
    LogoutAPIView,
    RegisterAPIView,
    VerifyOtpAPIView,
)

from .views.order_api import OrderViewSet
from .views.profile_api import ProfileAPIView
from .views.testimonial_api import TestimonialAPIView
from .views.company_setting_api import CompanySettingAPIView

from .views.chat_api import (
    AdminChatDetailAPIView,
    AdminChatListAPIView,
    AdminChatMessageAPIView,
    ClientChatAPIView,
)

from .views.newsletter_api import NewsletterAPIView


from .views.cart import (
    CartAddAPIView,
    CartAddBoissonAPIView,
    CartDetailAPIView,
    CartRemoveAPIView,
    CartUpdateAPIView,
    CartUpdateComponentAPIView,
)



app_name = "users_api"



router = DefaultRouter()

router.register(
    "addresses",
    AddressViewSet,
    basename="address",
)

router.register(
    "orders",
    OrderViewSet,
    basename="order",
)



urlpatterns = [

    # AUTH
    path(
        "auth/register/",
        RegisterAPIView.as_view(),
        name="register",
    ),

    path(
        "auth/verify-otp/",
        VerifyOtpAPIView.as_view(),
        name="verify-otp",
    ),

    path(
        "auth/login/",
        LoginAPIView.as_view(),
        name="login",
    ),

    path(
        "auth/logout/",
        LogoutAPIView.as_view(),
        name="logout",
    ),



    # PROFILE

    path(
        "profile/",
        ProfileAPIView.as_view(),
        name="profile",
    ),



    # CONTENT

    path(
        "testimonial/",
        TestimonialAPIView.as_view(),
        name="testimonial",
    ),


    path(
        "company-settings/",
        CompanySettingAPIView.as_view(),
        name="company-settings",
    ),


    path(
        "newsletter/",
        NewsletterAPIView.as_view(),
        name="newsletter",
    ),



    # CHAT CLIENT

    path(
        "chat/",
        ClientChatAPIView.as_view(),
        name="chat",
    ),



    # CHAT ADMIN

    path(
        "admin/chats/",
        AdminChatListAPIView.as_view(),
        name="admin-chat-list",
    ),

    path(
        "admin/chats/<uuid:conversation_id>/",
        AdminChatDetailAPIView.as_view(),
        name="admin-chat-detail",
    ),

    path(
        "admin/chats/<uuid:conversation_id>/messages/",
        AdminChatMessageAPIView.as_view(),
        name="admin-chat-message",
    ),



    # CART

    path(
        "cart/",
        CartDetailAPIView.as_view(),
        name="cart-list",
    ),


    path(
        "cart/add/",
        CartAddAPIView.as_view(),
        name="cart-add",
    ),


    path(
        "cart/remove/",
        CartRemoveAPIView.as_view(),
        name="cart-remove",
    ),


    path(
        "cart/update/",
        CartUpdateAPIView.as_view(),
        name="cart-update",
    ),


    path(
        "cart/update-component/",
        CartUpdateComponentAPIView.as_view(),
        name="cart-update-component",
    ),


    path(
        "cart/add-boisson/",
        CartAddBoissonAPIView.as_view(),
        name="cart-add-boisson",
    ),



    # ROUTER

    path(
        "",
        include(router.urls),
    ),
]
