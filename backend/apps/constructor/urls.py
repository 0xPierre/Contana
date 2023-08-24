from django.urls import path
from . import views

urlpatterns = [
    path("draft/", views.save_document_draft, name="save_document_draft"),
    path(
        "draft/<str:document_number>/",
        views.get_document_draft,
        name="get_document_draft",
    ),
    path("produce/", views.produce_document, name="produce_document"),
]
