from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"labels", views.LabelViewset, basename="clients")
router.register(r"", views.TaskViewset, basename="clients")

urlpatterns = [
    path("", include(router.urls)),
]
