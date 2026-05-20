"""Update UA therapy title, intro wording, step 1 and step 4 copy."""
from django.db import migrations, models


OLD_INTRO_FRAGMENT = "з\u2019ясовуємо"
NEW_INTRO_FRAGMENT = "розуміємо"


def forwards(apps, schema_editor):
    TherapyPage = apps.get_model("pages", "TherapyPage")
    TherapyStep = apps.get_model("pages", "TherapyStep")

    therapy = TherapyPage.objects.first()
    if not therapy:
        return

    therapy.title_uk = "Як проходить робота"
    therapy.intro_uk = (therapy.intro_uk or "").replace(
        OLD_INTRO_FRAGMENT, NEW_INTRO_FRAGMENT
    )
    therapy.save(update_fields=["title_uk", "intro_uk"])

    step1 = TherapyStep.objects.filter(page=therapy, order=1).first()
    if step1:
        step1.title_uk = "Призначаємо першу зустріч, де підписуємо інформовану згоду"
        step1.body_uk = ""
        step1.save(update_fields=["title_uk", "body_uk"])

    step4 = TherapyStep.objects.filter(page=therapy, order=4).first()
    if step4:
        step4.title_uk = "За потреби можливий формат разової консультації"
        step4.body_uk = (
            "зустріч, на якій ви отримуєте моє професійне бачення ситуації та, "
            "якщо потрібно, рекомендації щодо подальшого звернення."
        )
        step4.save(update_fields=["title_uk", "body_uk"])


def backwards(apps, schema_editor):
    TherapyPage = apps.get_model("pages", "TherapyPage")
    TherapyStep = apps.get_model("pages", "TherapyStep")

    therapy = TherapyPage.objects.first()
    if not therapy:
        return

    therapy.title_uk = "Як проходять зустрічі"
    therapy.intro_uk = (therapy.intro_uk or "").replace(
        NEW_INTRO_FRAGMENT, OLD_INTRO_FRAGMENT, 1
    )
    therapy.save(update_fields=["title_uk", "intro_uk"])

    step1 = TherapyStep.objects.filter(page=therapy, order=1).first()
    if step1:
        step1.title_uk = "Призначаємо першу зустріч"
        step1.body_uk = "де підписуємо інформовану згоду"
        step1.save(update_fields=["title_uk", "body_uk"])

    step4 = TherapyStep.objects.filter(page=therapy, order=4).first()
    if step4:
        step4.title_uk = "За потреби — разова консультація"
        step4.body_uk = (
            "зустріч, на якій ви отримуєте моє професійне бачення ситуації та, "
            "за потреби, рекомендації щодо подальшого звернення."
        )
        step4.save(update_fields=["title_uk", "body_uk"])


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0009_fix_therapy_intro_it_grammar"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
        migrations.AlterField(
            model_name="therapypage",
            name="title_uk",
            field=models.CharField(
                default="Як проходить робота",
                max_length=200,
                verbose_name="Заголовок (UA)",
            ),
        ),
    ]
