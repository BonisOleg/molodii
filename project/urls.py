"""Top-level URLconf with UA at root and IT at /it/ prefix."""
from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.core.views import healthz

urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz", healthz, name="healthz"),
    path("", include(("apps.pages.urls", "pages"), namespace="uk")),
    path("it/", include(("apps.pages.urls", "pages"), namespace="it")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
