from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView
from . import views

urlpatterns = [
    path("registration", views.user_registration, name="user_registration"),
    path("login", views.user_login, name="user_login"),
    path("refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout", TokenBlacklistView.as_view(), name="token_blacklist"),
    path(
        "password-reset-request",
        views.user_password_reset_request,
        name="user_password_reset_request",
    ),
    path(
        "password-reset",
        views.user_password_reset,
        name="user_password_reset",
    ),
    path(
        "update-profile",
        views.user_profil_update,
        name="user_profil_update",
    ),
    path(
        "update-password",
        views.user_password_update,
        name="user_password_update",
    ),
    path(
        "data",
        views.get_data,
        name="get_data",
    ),
]
