"""Add OfficePhoto model and attach Cernobbio cabinet images."""
from __future__ import annotations

from pathlib import Path

import django.db.models.deletion
from django.core.files import File
from django.db import migrations, models


CERNOBBIO_ASSETS = (
    ("interior-01.jpg", 0),
    ("interior-02.jpg", 1),
)


def attach_cernobbio_photos(apps, schema_editor):
    Office = apps.get_model("contacts", "Office")
    OfficePhoto = apps.get_model("contacts", "OfficePhoto")

    office = (
        Office.objects.filter(address_uk__icontains="Monti").first()
        or Office.objects.filter(city_uk__icontains="Черноббіо").first()
    )
    if not office or OfficePhoto.objects.filter(office=office).exists():
        return

    assets_dir = Path(__file__).resolve().parent.parent / "office_assets" / "cernobbio"
    for filename, order in CERNOBBIO_ASSETS:
        path = assets_dir / filename
        if not path.is_file():
            continue
        with path.open("rb") as handle:
            photo = OfficePhoto(office=office, order=order)
            photo.image.save(filename, File(handle), save=True)


def detach_cernobbio_photos(apps, schema_editor):
    Office = apps.get_model("contacts", "Office")
    OfficePhoto = apps.get_model("contacts", "OfficePhoto")

    office = (
        Office.objects.filter(address_uk__icontains="Monti").first()
        or Office.objects.filter(city_uk__icontains="Черноббіо").first()
    )
    if office:
        OfficePhoto.objects.filter(office=office).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0003_add_consultation_request"),
    ]

    operations = [
        migrations.CreateModel(
            name="OfficePhoto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="offices/", verbose_name="Фото")),
                ("order", models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")),
                (
                    "office",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="photos",
                        to="contacts.office",
                        verbose_name="Кабінет",
                    ),
                ),
            ],
            options={
                "verbose_name": "Фото кабінету",
                "verbose_name_plural": "Фото кабінетів",
                "ordering": ["order", "id"],
            },
        ),
        migrations.RunPython(attach_cernobbio_photos, detach_cernobbio_photos),
    ]
