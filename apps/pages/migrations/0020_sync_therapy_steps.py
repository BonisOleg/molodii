"""Sync therapy steps when production still has legacy seed_demo copy."""
from django.db import migrations

from apps.pages.therapy_content import (
    THERAPY_PRICING_NOTE_IT,
    THERAPY_PRICING_NOTE_UK,
    THERAPY_STEPS,
    THERAPY_TITLE_IT,
    THERAPY_TITLE_UK,
    therapy_steps_are_stale,
)


def _sync_steps(TherapyStep, page):
    TherapyStep.objects.filter(page=page).delete()
    for order, data in enumerate(THERAPY_STEPS, start=1):
        TherapyStep.objects.create(page=page, order=order, **data)


def forwards(apps, schema_editor):
    TherapyPage = apps.get_model("pages", "TherapyPage")
    TherapyStep = apps.get_model("pages", "TherapyStep")

    page = TherapyPage.objects.first()
    if not page:
        return

    steps = TherapyStep.objects.filter(page=page).order_by("order", "id")
    if not therapy_steps_are_stale(steps):
        return

    page.title_uk = THERAPY_TITLE_UK
    page.title_it = THERAPY_TITLE_IT
    page.pricing_note_uk = THERAPY_PRICING_NOTE_UK
    page.pricing_note_it = THERAPY_PRICING_NOTE_IT
    page.save(
        update_fields=[
            "title_uk",
            "title_it",
            "pricing_note_uk",
            "pricing_note_it",
        ]
    )
    _sync_steps(TherapyStep, page)


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0019_sync_services_bullet_topics"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
