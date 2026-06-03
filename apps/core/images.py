"""Resolve page images: admin upload when present, otherwise bundled static files."""
from __future__ import annotations

from django.db.models.fields.files import FieldFile
from django.templatetags.static import static


def display_image_url(field: FieldFile | None, static_path: str) -> str:
    """URL for templates: uploaded file if it exists on storage, else ``static()``."""
    if field:
        try:
            name = field.name
            if name and field.storage.exists(name):
                return field.url
        except (ValueError, OSError):
            pass
    return static(static_path)
