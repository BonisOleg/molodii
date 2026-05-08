"""Inject language and site settings into all templates."""
from __future__ import annotations

from django.conf import settings

from .models import SiteSettings


def lang_context(request):
    lang = getattr(request, "lang", settings.DEFAULT_LANG)
    other = "it" if lang == "uk" else "uk"

    path = request.path or "/"
    if lang == "uk":
        alt_path = "/it" + path if path.startswith("/") else f"/it/{path}"
        if alt_path == "/it":
            alt_path = "/it/"
    else:
        alt_path = path[3:] if path.startswith("/it/") else path.replace("/it", "/", 1)
        if not alt_path.startswith("/"):
            alt_path = "/" + alt_path
        if alt_path == "":
            alt_path = "/"
    return {
        "LANG": lang,
        "OTHER_LANG": other,
        "ALT_LANG_URL": alt_path,
        "SUPPORTED_LANGS": settings.SUPPORTED_LANGS,
    }


def site_settings(request):
    try:
        obj = SiteSettings.load()
    except Exception:
        obj = None
    return {"site_settings": obj}
