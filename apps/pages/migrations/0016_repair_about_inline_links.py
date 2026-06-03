"""Repair AboutPage education/approach when seed_demo ran before data migrations."""
from django.db import migrations

from apps.pages.about_content import (
    APPROACH_IT,
    APPROACH_UK,
    EDUCATION_IT,
    EDUCATION_UK,
    approach_has_raw_url,
    education_has_raw_url,
)


def forwards(apps, schema_editor):
    AboutPage = apps.get_model("pages", "AboutPage")
    page = AboutPage.objects.first()
    if not page:
        return

    update_fields: list[str] = []
    if education_has_raw_url(page.education_uk or ""):
        page.education_uk = EDUCATION_UK
        update_fields.append("education_uk")
    if education_has_raw_url(page.education_it or ""):
        page.education_it = EDUCATION_IT
        update_fields.append("education_it")
    if approach_has_raw_url(page.approach_uk or ""):
        page.approach_uk = APPROACH_UK
        update_fields.append("approach_uk")
    if approach_has_raw_url(page.approach_it or ""):
        page.approach_it = APPROACH_IT
        update_fields.append("approach_it")

    if update_fields:
        page.save(update_fields=update_fields)


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0015_update_about_approach_links"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
