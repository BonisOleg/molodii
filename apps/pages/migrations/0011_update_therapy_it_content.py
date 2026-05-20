"""Update IT therapy title and step copy to match UA changes from 0010."""
from django.db import migrations


def forwards(apps, schema_editor):
    TherapyPage = apps.get_model("pages", "TherapyPage")
    TherapyStep = apps.get_model("pages", "TherapyStep")

    therapy = TherapyPage.objects.first()
    if not therapy:
        return

    therapy.title_it = "Come si svolge il lavoro"
    therapy.save(update_fields=["title_it"])

    step1 = TherapyStep.objects.filter(page=therapy, order=1).first()
    if step1:
        step1.title_it = "Fissiamo il primo incontro, in cui firmiamo il consenso informato"
        step1.body_it = ""
        step1.save(update_fields=["title_it", "body_it"])

    step4 = TherapyStep.objects.filter(page=therapy, order=4).first()
    if step4:
        step4.title_it = "Se necessario è possibile una consulenza singola"
        step4.body_it = (
            "un incontro in cui ricevete una lettura professionale della situazione e, "
            "se necessario, indicazioni su come proseguire."
        )
        step4.save(update_fields=["title_it", "body_it"])


def backwards(apps, schema_editor):
    TherapyPage = apps.get_model("pages", "TherapyPage")
    TherapyStep = apps.get_model("pages", "TherapyStep")

    therapy = TherapyPage.objects.first()
    if not therapy:
        return

    therapy.title_it = "Come procedono gli incontri"
    therapy.save(update_fields=["title_it"])

    step1 = TherapyStep.objects.filter(page=therapy, order=1).first()
    if step1:
        step1.title_it = "Fissiamo il primo incontro"
        step1.body_it = "in cui firmiamo il consenso informato"
        step1.save(update_fields=["title_it", "body_it"])

    step4 = TherapyStep.objects.filter(page=therapy, order=4).first()
    if step4:
        step4.title_it = "Se necessario — consulenza singola"
        step4.body_it = (
            "un incontro in cui ricevete una lettura professionale della situazione e, "
            "se serve, indicazioni su come proseguire."
        )
        step4.save(update_fields=["title_it", "body_it"])


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0010_update_therapy_uk_content"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
