from django.urls import path
from restaurants.users.views.auth_views import CustomLogoutView

from restaurants.users.views.auth_views import RegisterView, VerifyOtpView
from restaurants.users.views.home_view import HomeView

from .views.login_views import LoginChoiceView, LoginView, ClientDashboardView, AdminDashboardView
app_name = "users"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
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
