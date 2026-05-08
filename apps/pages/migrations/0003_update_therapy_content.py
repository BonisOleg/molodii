from django.db import migrations

INTRO_UK = (
    "15-хвилинна безкоштовна розмова. На ній ми разом розуміємо, з чим ви приходите, "
    "який напрямок роботи може бути доречним і чи підходимо ми одне одному. "
    "Також визначаємо формат: онлайн або особисто в Мілані чи Комо, "
    "та мову роботи — українську або італійську."
)

STEPS_UK = [
    {
        "order": 1,
        "title_uk": "Призначаємо першу зустріч",
        "body_uk": "де підписуємо інформовану згоду",
    },
    {
        "order": 2,
        "title_uk": "На перших зустрічах окреслюємо запит і визначаємо цілі",
        "body_uk": "",
    },
    {
        "order": 3,
        "title_uk": "Поступово формуємо процес, у якому рухаємось до змін",
        "body_uk": "",
    },
    {
        "order": 4,
        "title_uk": "Разова консультація",
        "body_uk": (
            "За потреби можливий формат разової консультації — зустріч, на якій ви отримуєте "
            "моє професійне бачення ситуації та, якщо потрібно, рекомендації щодо подальшого звернення."
        ),
    },
]


def update_therapy_content(apps, schema_editor):
    TherapyPage = apps.get_model("pages", "TherapyPage")
    TherapyStep = apps.get_model("pages", "TherapyStep")

    page = TherapyPage.objects.first()
    if page is None:
        return

    page.intro_uk = INTRO_UK
    page.save(update_fields=["intro_uk"])

    TherapyStep.objects.filter(page=page).delete()

    for data in STEPS_UK:
        TherapyStep.objects.create(page=page, **data)


def revert_therapy_content(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0002_update_therapy_title"),
    ]

    operations = [
        migrations.RunPython(update_therapy_content, revert_therapy_content),
    ]
