"""Determine active language from URL namespace."""
from __future__ import annotations

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class LanguageFromUrlMiddleware(MiddlewareMixin):
    """Set ``request.lang`` based on the URL namespace (uk | it).

    Falls back to the default language. Runs after URL resolution by
    examining ``resolver_match`` in ``process_view``.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        namespace = getattr(getattr(request, "resolver_match", None), "namespace", "")
        request.lang = namespace if namespace in settings.SUPPORTED_LANGS else settings.DEFAULT_LANG
        return None

    def process_request(self, request):
        request.lang = settings.DEFAULT_LANG
