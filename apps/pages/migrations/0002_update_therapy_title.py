from django.db import migrations


def update_therapy_title(apps, schema_editor):
    TherapyPage = apps.get_model("pages", "TherapyPage")
    TherapyPage.objects.filter(title_uk="Як проходить терапія").update(
        title_uk="Як проходять зустрічі"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(update_therapy_title, migrations.RunPython.noop),
    ]
