"""Resolve page images: admin upload when present, otherwise bundled static files."""
from __future__ import annotations

from django.conf import settings
from django.db.models.fields.files import FieldFile
from django.templatetags.static import static


def media_is_served() -> bool:
    """Uploaded files are only linked when the app can serve MEDIA (local DEBUG)."""
    return settings.DEBUG or getattr(settings, "SERVE_MEDIA", False)


def display_image_url(field: FieldFile | None, static_path: str) -> str:
    """URL for templates: uploaded file if served and on storage, else ``static()``."""
    if field and media_is_served():
        try:
            name = field.name
            if name and field.storage.exists(name):
                return field.url
        except (ValueError, OSError):
            pass
    return static(static_path)
