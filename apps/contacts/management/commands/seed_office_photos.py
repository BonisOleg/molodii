"""Upload bundled Cernobbio office photos to the active media storage (e.g. Cloudinary)."""
from __future__ import annotations

from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from apps.contacts.models import Office, OfficePhoto

ASSETS_DIR = Path(__file__).resolve().parents[2] / "office_assets" / "cernobbio"
FILES = (
    ("interior-01.jpg", 0),
    ("interior-02.jpg", 1),
)


class Command(BaseCommand):
    help = "Upload Cernobbio cabinet photos to media storage when missing."

    def handle(self, *args, **options):
        office = (
            Office.objects.filter(address_uk__icontains="Monti").first()
            or Office.objects.filter(city_uk__icontains="Черноббіо").first()
        )
        if not office:
            self.stdout.write(self.style.WARNING("Cernobbio office not found."))
            return

        existing = OfficePhoto.objects.filter(office=office).count()
        if existing >= len(FILES):
            self.stdout.write("Cernobbio photos already present, skipping.")
            return

        OfficePhoto.objects.filter(office=office).delete()

        uploaded = 0
        for filename, order in FILES:
            path = ASSETS_DIR / filename
            if not path.is_file():
                self.stderr.write(f"Missing asset: {path}")
                continue
            try:
                with path.open("rb") as handle:
                    photo = OfficePhoto(office=office, order=order)
                    photo.image.save(filename, File(handle), save=True)
                    uploaded += 1
                    self.stdout.write(f"Uploaded {filename} -> {photo.image.url}")
            except Exception as exc:
                self.stderr.write(
                    self.style.WARNING(f"Skipped {filename}: {exc}")
                )

        if uploaded:
            self.stdout.write(self.style.SUCCESS("Cernobbio office photos uploaded."))
        else:
            self.stdout.write(
                self.style.WARNING(
                    "No photos uploaded (static fallback will be used on the site)."
                )
            )
