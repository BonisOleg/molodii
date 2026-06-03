"""Repair Services page when seed_demo left legacy card-style items."""
from django.db import migrations

from apps.pages.services_content import (
    SERVICE_ITEMS_IT,
    SERVICE_ITEMS_UK,
    SERVICES_INTRO_IT,
    SERVICES_INTRO_UK,
    SERVICES_OUTRO_IT,
    SERVICES_OUTRO_UK,
    services_items_are_stale,
)


def _sync_items(ServiceItem, page):
    ServiceItem.objects.filter(page=page).delete()
    for i, (title_uk, title_it) in enumerate(zip(SERVICE_ITEMS_UK, SERVICE_ITEMS_IT)):
        ServiceItem.objects.create(
            page=page,
            order=i,
            title_uk=title_uk,
            title_it=title_it,
            description_uk="",
            description_it="",
        )


def forwards(apps, schema_editor):
    ServicesPage = apps.get_model("pages", "ServicesPage")
    ServiceItem = apps.get_model("pages", "ServiceItem")

    page = ServicesPage.objects.first()
    if not page:
        return

    items = ServiceItem.objects.filter(page=page).order_by("order", "id")
    if not services_items_are_stale(items):
        return

    page.intro_uk = SERVICES_INTRO_UK
    page.intro_it = SERVICES_INTRO_IT
    page.outro_uk = SERVICES_OUTRO_UK
    page.outro_it = SERVICES_OUTRO_IT
    page.save(update_fields=["intro_uk", "intro_it", "outro_uk", "outro_it"])
    _sync_items(ServiceItem, page)


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0016_repair_about_inline_links"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
