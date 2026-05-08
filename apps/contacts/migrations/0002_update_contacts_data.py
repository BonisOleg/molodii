"""Update contacts: clear schedule, fix office addresses, update site credentials."""
from django.db import migrations


OFFICES = [
    {
        "order": 0,
        "city_uk": "Мілан",
        "city_it": "Milano",
        "address_uk": "Via delle Camelie 12",
        "address_it": "Via delle Camelie 12",
        "map_url": "https://maps.google.com/?q=Via+delle+Camelie+12+Milano",
    },
    {
        "order": 1,
        "city_uk": "Черноббіо (CO)",
        "city_it": "Cernobbio (CO)",
        "address_uk": "Via Vincenzo Monti 4",
        "address_it": "Via Vincenzo Monti 4",
        "map_url": "https://maps.google.com/?q=Via+Vincenzo+Monti+4+Cernobbio",
    },
]


def update_contacts(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    ContactsPage = apps.get_model("contacts", "ContactsPage")
    Office = apps.get_model("contacts", "Office")

    site = SiteSettings.objects.first()
    if site:
        site.email = "molodiitetiana@gmail.com"
        site.phone = "+393274470996"
        site.save(update_fields=["email", "phone"])

    contacts = ContactsPage.objects.first()
    if contacts:
        contacts.working_hours_uk = ""
        contacts.working_hours_it = ""
        contacts.save(update_fields=["working_hours_uk", "working_hours_it"])

    Office.objects.all().delete()
    for data in OFFICES:
        Office.objects.create(**data)


def revert_contacts(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0001_initial"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(update_contacts, revert_contacts),
    ]
