"""Production settings (Render)."""
from __future__ import annotations

import os

from .base import *  # noqa: F401,F403

DEBUG = False

SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True").lower() == "true"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

# Render інжектує RENDER_EXTERNAL_HOSTNAME / RENDER_EXTERNAL_URL на web-сервісі.
_render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "").strip()
if _render_host and _render_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS = [*ALLOWED_HOSTS, _render_host]

_render_url = os.environ.get("RENDER_EXTERNAL_URL", "").strip().rstrip("/")
if _render_url and _render_url not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = [*CSRF_TRUSTED_ORIGINS, _render_url]
