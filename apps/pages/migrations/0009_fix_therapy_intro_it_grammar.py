"""Fix IT therapy intro wording after 0007."""
from django.db import migrations


OLD = (
    "Insieme chiarite con cosa arrivate, quale direzione di lavoro può essere adatta e se siamo compatibili."
)
NEW = (
    "Insieme capiamo con cosa arrivate, quale direzione di lavoro può essere adatta e se siamo compatibili."
)


def forwards(apps, schema_editor):
    TherapyPage = apps.get_model("pages", "TherapyPage")
    p = TherapyPage.objects.first()
    if p and OLD in (p.intro_it or ""):
        p.intro_it = (p.intro_it or "").replace(OLD, NEW)
        p.save(update_fields=["intro_it"])


def backwards(apps, schema_editor):
    TherapyPage = apps.get_model("pages", "TherapyPage")
    p = TherapyPage.objects.first()
    if p and NEW in (p.intro_it or ""):
        p.intro_it = (p.intro_it or "").replace(NEW, OLD)
        p.save(update_fields=["intro_it"])


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0008_alter_servicespage_options_alter_therapystep_options_and_more"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
