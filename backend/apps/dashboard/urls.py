from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


urlpatterns = [
    path("cards-data", views.get_cards_data, name="get_cards_data"),
    path("turnover-chart", views.get_turnover_chart, name="get_turnover_chart"),
    path(
        "best-articles-chart",
        views.get_best_articles_chart,
        name="get_best_articles_chart",
    ),
    path(
        "best-clients-chart",
        views.get_best_clients_chart,
        name="get_best_clients_chart",
    ),
]
