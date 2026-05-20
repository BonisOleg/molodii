"""Стабільний dev-сервер: без autoreload за замовчуванням.

Перезапуск процесу при зміні файлів часто обриває фоновий термінал або IDE.
Шаблони й статика в DEBUG підхоплюються без Python-релоаду.

Autoreload як у стандартному Django:
  DJANGO_DEV_RELOADER=1 python3 manage.py runserver …
"""
from __future__ import annotations

import os

from django.contrib.staticfiles.management.commands.runserver import (
    Command as StaticfilesRunserverCommand,
)


class Command(StaticfilesRunserverCommand):
    def handle(self, *args, **options):
        if os.environ.get("DJANGO_DEV_RELOADER", "").lower() not in ("1", "true", "yes"):
            options["use_reloader"] = False
        return super().handle(*args, **options)
