"""Office galleries use bundled static files (static/img/offices/)."""
from __future__ import annotations

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "No-op: Milan/Cernobbio photos are in static/img/offices/."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(
                "Office photos are served from static/img/offices/; nothing to upload."
            )
        )
