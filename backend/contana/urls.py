"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("contana_admin_pr8d47awqfthgfpmnvtHzs/", admin.site.urls),
    path("api/user/", include("apps.user.urls")),
    path(
        "",
        include("apps.entreprise.urls"),
    ),
    path("api/entreprise/<str:entreprise_slug>/clients/", include("apps.clients.urls")),
    path(
        "api/entreprise/<str:entreprise_slug>/constructor/",
        include("apps.constructor.urls"),
    ),
    path(
        "api/entreprise/<str:entreprise_slug>/documents/",
        include("apps.documents.urls"),
    ),
    path(
        "api/entreprise/<str:entreprise_slug>/dashboard/",
        include("apps.dashboard.urls"),
    ),
    path(
        "api/entreprise/<str:entreprise_slug>/tasks/",
        include("apps.tasks.urls"),
    ),
] + static(settings.STATIC_URL)
