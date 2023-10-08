from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r"catalog/template-categories", views.TemplateCategoriesViewSet, basename="template"
)

urlpatterns = [
    path("", include(router.urls)),
    path("draft/", views.save_document_draft, name="save_document_draft"),
    path(
        "draft/<str:document_number>/",
        views.get_document_draft,
        name="get_document_draft",
    ),
    path("produce/", views.produce_document, name="produce_document"),
    path("preview/", views.produce_document_preview, name="produce_document_preview"),
    path("catalog/", views.get_catalog, name="get_catalog"),
    path("catalog/template/", views.create_template, name="create_template"),
    path(
        "catalog/template/<int:template_id>/",
        views.update_template,
        name="update_template",
    ),
    path(
        "catalog/template/<int:template_id>/delete",
        views.delete_template,
        name="delete_template",
    ),
    # path("catalog/template/")
]
