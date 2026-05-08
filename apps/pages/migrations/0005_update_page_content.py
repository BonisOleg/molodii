"""Update all UA text content per client brief."""
from django.db import migrations


HERO_TITLE_UK = "Простір, де ви зможете краще зрозуміти себе та почати жити більш усвідомлено."

HERO_SUBTITLE_UK = (
    "Я психологиня, яка працює в Італії та народжена в Україні. "
    "Працюю з людьми у період кризи, змін та еміграції."
)

POSITIONING_UK = (
    "«Справжня подорож полягає не в пошуку нових земель, а в новому погляді.» — Марсель Пруст"
)

ABOUT_LEAD_UK = (
    "Мій підхід формується не лише через професійну підготовку, але й через особистий досвід "
    "адаптації в новій країні та роботу в міжкультурному контексті."
)

ABOUT_BODY_UK = (
    "У своїй практиці я працювала з:\n"
    "• людьми на різних етапах еміграції\n"
    "• ситуаціями домашнього насильства\n"
    "• онкохворими пацієнтами та їхніми сім'ями\n"
    "• парами з різним культурним і національним контекстом"
)

ABOUT_EDUCATION_UK = (
    "вища освіта в Україні та Італії. Зареєстрована в Ордені психологів Ломбардії. "
    "https://www.opl.it/psicologi/28919/Molodii-Tetiana"
)

ABOUT_APPROACH_UK = (
    "Я працюю відповідно до етичного кодексу італійських психологів "
    "https://www.psy.it/la-professione-psicologica/codice-deontologico-degli-psicologi-italiani/"
    "codice-deontologico-vigente/ який гарантує конфіденційність, повагу до людини та її контексту, "
    "а також відповідальність за межі власної компетенції і постійний професійний розвиток.\n\n"
    "Я працюю в когнітивно-конструктивістському підході, що фокусується на тому, як людина формує "
    "своє бачення реальності та які значення надає власному досвіду.\n\n"
    "У роботі я також використовую майндфулнес і роботу з тілом — як спосіб повернутися до себе, "
    "краще відчути свій стан і поступово відновити внутрішню опору, навіть після складних "
    "життєвих періодів."
)

SERVICES_TITLE_UK = "З чим я працюю"

SERVICES_INTRO_UK = "Ви можете звернутися до мене, якщо відчуваєте:"

SERVICES_OUTRO_UK = (
    "Не потрібно бути в критичному стані, щоб звернутися до мене. "
    "Іноді достатньо відчути, що звичні способи більше не працюють і дати собі час та простір "
    "поступово знайти нові.\n\n"
    "Напишіть мені для того щоб дізнатись вартість зустрічей."
)

SERVICE_ITEMS_UK = [
    "труднощі адаптації до нової країни, культури або життєвого етапу",
    "розгубленість, пов'язану з еміграцією чи змінами в житті",
    "травматичний досвід, який продовжує впливати на сьогодення",
    "складнощі у стосунках, емоційну залежність або розставання",
    "втрату опори в собі, зниження віри в себе",
    "низьку самооцінку",
    "емоційне виснаження або вигорання",
    "втрату близької людини, процес горювання",
    "тривожні або депресивні стани",
]

THERAPY_INTRO_UK = (
    "15-хвилинна безкоштовної розмови. "
    "На ній ми разом розуміємо, з чим ви приходите, який напрямок роботи може бути доречним "
    "і чи підходимо ми одне одному.\n\n"
    "Також визначаємо формат: онлайн або особисто в Мілані чи Комо, "
    "та мову роботи — українську або італійську."
)

TAGLINE_UK = "підтримка для дорослих– онлайн та вживу(Мілан, Комо)"


def update_content(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    HomePage = apps.get_model("pages", "HomePage")
    AboutPage = apps.get_model("pages", "AboutPage")
    ServicesPage = apps.get_model("pages", "ServicesPage")
    ServiceItem = apps.get_model("pages", "ServiceItem")
    TherapyPage = apps.get_model("pages", "TherapyPage")

    site = SiteSettings.objects.first()
    if site:
        site.tagline_uk = TAGLINE_UK
        site.save(update_fields=["tagline_uk"])

    home = HomePage.objects.first()
    if home:
        home.hero_title_uk = HERO_TITLE_UK
        home.hero_subtitle_uk = HERO_SUBTITLE_UK
        home.positioning_uk = POSITIONING_UK
        home.save(update_fields=["hero_title_uk", "hero_subtitle_uk", "positioning_uk"])

    about = AboutPage.objects.first()
    if about:
        about.lead_uk = ABOUT_LEAD_UK
        about.body_uk = ABOUT_BODY_UK
        about.education_uk = ABOUT_EDUCATION_UK
        about.approach_uk = ABOUT_APPROACH_UK
        about.save(update_fields=["lead_uk", "body_uk", "education_uk", "approach_uk"])

    services = ServicesPage.objects.first()
    if services:
        services.title_uk = SERVICES_TITLE_UK
        services.intro_uk = SERVICES_INTRO_UK
        services.outro_uk = SERVICES_OUTRO_UK
        services.save(update_fields=["title_uk", "intro_uk", "outro_uk"])

        ServiceItem.objects.filter(page=services).delete()
        for i, title in enumerate(SERVICE_ITEMS_UK):
            ServiceItem.objects.create(
                page=services,
                order=i,
                title_uk=title,
                title_it="",
                description_uk="",
                description_it="",
            )

    therapy = TherapyPage.objects.first()
    if therapy:
        therapy.intro_uk = THERAPY_INTRO_UK
        therapy.save(update_fields=["intro_uk"])


def revert_content(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0004_servicespage_outro"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(update_content, revert_content),
    ]
