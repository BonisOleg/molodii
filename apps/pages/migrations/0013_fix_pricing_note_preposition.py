"""Fix preposition: 'на знайомстві' → 'при знайомстві' in therapy pricing note."""
from django.db import migrations

OLD_UK = (
    "Сесія триває 50 хвилин. Регулярність — раз на тиждень. "
    "Вартість і деталі обговорюємо на знайомстві."
)
NEW_UK = (
    "Сесія триває 50 хвилин. Регулярність — раз на тиждень. "
    "Вартість і деталі обговорюємо при знайомстві."
)


def forwards(apps, schema_editor):
    TherapyPage = apps.get_model("pages", "TherapyPage")
    page = TherapyPage.objects.first()
    if not page:
        return
    if page.pricing_note_uk == OLD_UK:
        page.pricing_note_uk = NEW_UK
        page.save(update_fields=["pricing_note_uk"])


def backwards(apps, schema_editor):
    TherapyPage = apps.get_model("pages", "TherapyPage")
    page = TherapyPage.objects.first()
    if not page:
        return
    if page.pricing_note_uk == NEW_UK:
        page.pricing_note_uk = OLD_UK
        page.save(update_fields=["pricing_note_uk"])


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0012_update_about_education"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
