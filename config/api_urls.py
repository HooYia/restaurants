"""
URLConf réservée au serveur API.
Aucune page HTML du site web.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [

    # Toutes les API
    path(
        "api/",
        include("config.api_router"),
    ),


    # Documentation OpenAPI / Swagger
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="api-schema",
    ),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="api-schema"
        ),
        name="api-docs",
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
