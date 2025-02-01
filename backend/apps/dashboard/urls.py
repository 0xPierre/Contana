from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


urlpatterns = [
    path("cards-data", views.get_cards_data, name="get_cards_data"),
    path("turnover-chart", views.get_turnover_chart, name="get_turnover_chart"),
    path(
        "best-clients-by-signed-quotes",
        views.get_best_clients_by_signed_quotes,
        name="get_best_clients_by_signed_quotes",
    ),
    path(
        "best-user-by-signed-quotes",
        views.get_best_user_by_signed_quotes,
        name="get_best_user_by_signed_quotes",
    ),
    path(
        "outstanding-quote-by-commercial",
        views.get_outstanding_quote_by_commercial,
        name="get_outstanding_quote_by_commercial",
    ),
]
