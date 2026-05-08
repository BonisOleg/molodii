"""Polish UA copy, fix ethics URL, add full IT strings, set brand names."""
from django.db import migrations, models


ETHICS_URL = (
    "https://www.psy.it/la-professione-psicologica/"
    "codice-deontologico-degli-psicologi-italiani/codice-deontologico-vigente/"
)

TAGLINE_UK = "Підтримка для дорослих – онлайн та вживу (Мілан, Комо)"
TAGLINE_IT = "Supporto per adulti – online e di persona (Milano, Como)"

BRAND_UK = "Психолог – Молодій Тетяна"
BRAND_IT = "Psicologa – Molodii Tetiana"

HERO_TITLE_UK = (
    "Простір, де ви зможете краще зрозуміти себе та почати жити більш усвідомлено."
)
HERO_TITLE_IT = (
    "Uno spazio dove puoi conoscerti meglio e iniziare a vivere in modo più consapevole."
)

HERO_SUBTITLE_UK = (
    "Я психологиня, яка працює в Італії та народжена в Україні. "
    "Працюю з людьми у період кризи, змін та еміграції."
)
HERO_SUBTITLE_IT = (
    "Sono psicologa, lavoro in Italia e sono nata in Ucraina. "
    "Accompagno le persone in periodi di crisi, cambiamento ed emigrazione."
)

POSITIONING_UK = (
    "«Справжня подорож полягає не в пошуку нових земель, а в новому погляді.» — Марсель Пруст"
)
POSITIONING_IT = (
    "«Il vero viaggio di scoperta non consiste nel cercare nuove terre, "
    "ma nell'avere nuovi occhi.» — Marcel Proust"
)

ABOUT_LEAD_UK = (
    "Мій підхід формується не лише через професійну підготовку, але й через особистий досвід "
    "адаптації в новій країні та роботу в міжкультурному контексті."
)
ABOUT_LEAD_IT = (
    "Il mio modo di lavorare nasce non solo dalla formazione professionale, "
    "ma anche dall'esperienza personale di adattamento in un nuovo paese e dal lavoro in contesti interculturali."
)

ABOUT_BODY_UK = (
    "У своїй практиці я працювала з:\n"
    "• людьми на різних етапах еміграції\n"
    "• ситуаціями домашнього насильства\n"
    "• онкохворими пацієнтами та їхніми сім’ями\n"
    "• парами з різним культурним і національним контекстом"
)
ABOUT_BODY_IT = (
    "Nella mia pratica ho lavorato con:\n"
    "• persone in diversi momenti dell'emigrazione\n"
    "• situazioni di violenza domestica\n"
    "• pazienti oncologici e le loro famiglie\n"
    "• coppie con diverso contesto culturale e nazionale"
)

ABOUT_EDUCATION_UK = (
    "Вища освіта в Україні та Італії. Зареєстрована в Ордені психологів Ломбардії. "
    "https://www.opl.it/psicologi/28919/Molodii-Tetiana"
)
ABOUT_EDUCATION_IT = (
    "Laurea in Ucraina e in Italia. Iscritta all'Ordine degli Psicologi della Lombardia. "
    "https://www.opl.it/psicologi/28919/Molodii-Tetiana"
)

ABOUT_APPROACH_UK = (
    "Я працюю відповідно до етичного кодексу італійських психологів "
    f"{ETHICS_URL}"
    " який гарантує конфіденційність, повагу до людини та її контексту, "
    "а також відповідальність за межі власної компетенції й постійний професійний розвиток.\n\n"
    "Я працюю в когнітивно-конструктивістському підході, що зосереджується на тому, як людина формує "
    "своє бачення реальності та які значення надає власному досвіду.\n\n"
    "У роботі я також використовую майндфулнес і роботу з тілом — як спосіб повернутися до себе, "
    "краще відчути свій стан і поступово відновити внутрішню опору, навіть після складних "
    "життєвих періодів."
)
ABOUT_APPROACH_IT = (
    "Mi attengo al codice deontologico degli psicologi italiani "
    f"({ETHICS_URL}), "
    "che garantisce riservatezza, rispetto della persona e del suo contesto, responsabilità sui limiti "
    "di competenza e aggiornamento professionale continuo.\n\n"
    "Lavoro nell'approccio cognitivo-costruttivista, con attenzione a come la persona costruisce la realtà "
    "e attribuisce significato alla propria esperienza.\n\n"
    "Utilizzo anche mindfulness e il lavoro sul corpo — per tornare a sé, percepire meglio il proprio stato "
    "e gradualmente ritrovare un sostegno interno, anche dopo periodi difficili."
)

SERVICES_TITLE_UK = "З чим я працюю"
SERVICES_TITLE_IT = "Con cosa lavoro"

SERVICES_INTRO_UK = "Ви можете звернутися до мене, якщо відчуваєте:"
SERVICES_INTRO_IT = "Puoi rivolgerti a me se provi:"

SERVICES_OUTRO_UK = (
    "Не потрібно бути в критичному стані, щоб звернутися до мене. "
    "Іноді достатньо відчути, що звичні способи більше не працюють, і дати собі час і простір, "
    "щоб поступово знайти нові.\n\n"
    "Напишіть мені, щоб дізнатися вартість зустрічей."
)
SERVICES_OUTRO_IT = (
    "Non è necessario trovarsi in una condizione critica per contattarmi. "
    "A volte basta accorgersi che le abituali strategie non funzionano più e concedersi tempo e spazio "
    "per trovarne di nuove, gradualmente.\n\n"
    "Scrivimi per conoscere le tariffe degli incontri."
)

SERVICE_ITEMS_UK = [
    "труднощі адаптації до нової країни, культури або життєвого етапу",
    "розгубленість, пов’язану з еміграцією чи змінами в житті",
    "травматичний досвід, який продовжує впливати на сьогодення",
    "складнощі в стосунках, емоційну залежність або розставання",
    "втрату опори в собі, зниження віри в себе",
    "низьку самооцінку",
    "емоційне виснаження або вигорання",
    "втрату близької людини, процес горювання",
    "тривожні або депресивні стани",
]

SERVICE_ITEMS_IT = [
    "difficoltà di adattamento a un nuovo paese, cultura o fase della vita",
    "disorientamento legato all'emigrazione o ai cambiamenti nella vita",
    "un'esperienza traumatica che continua a influenzare il presente",
    "difficoltà nelle relazioni, dipendenza affettiva o separazione",
    "perdita di sostegno interiore, calo della fiducia in sé stessi",
    "bassa autostima",
    "esaurimento emotivo o burnout",
    "perdita di una persona cara, processo di lutto",
    "stati d'ansia o di depressione",
]

THERAPY_TITLE_IT = "Come procedono gli incontri"

THERAPY_INTRO_UK = (
    "15-хвилинна безкоштовна розмова. "
    "На ній ми разом з’ясовуємо, з чим ви приходите, який напрямок роботи може бути доречним "
    "і чи підходимо ми одне одному.\n\n"
    "Також визначаємо формат: онлайн або особисто в Мілані чи Комо, "
    "та мову роботи — українську або італійську."
)
THERAPY_INTRO_IT = (
    "Una conversazione gratuita di 15 minuti. "
    "Insieme capiamo con cosa arrivate, quale direzione di lavoro può essere adatta e se siamo compatibili.\n\n"
    "Definiamo anche la modalità: online o di persona a Milano o Como, "
    "e la lingua di lavoro — ucraina o italiana."
)

STEPS_UK_IT = [
    (
        "Призначаємо першу зустріч",
        "Fissiamo il primo incontro",
        "де підписуємо інформовану згоду",
        "in cui firmiamo il consenso informato",
    ),
    (
        "На перших зустрічах окреслюємо запит і визначаємо цілі",
        "Nei primi incontri delimitiamo la richiesta e definiamo gli obiettivi",
        "",
        "",
    ),
    (
        "Поступово формуємо процес, у якому рухаємось до змін",
        "Gradualmente costruiamo un percorso in cui ci muoviamo verso il cambiamento",
        "",
        "",
    ),
    (
        "За потреби — разова консультація",
        "Se necessario — consulenza singola",
        (
            "зустріч, на якій ви отримуєте моє професійне бачення ситуації та, за потреби, "
            "рекомендації щодо подальшого звернення."
        ),
        (
            "un incontro in cui ricevete una lettura professionale della situazione e, se serve, "
            "indicazioni su come proseguire."
        ),
    ),
]


def forwards(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    HomePage = apps.get_model("pages", "HomePage")
    AboutPage = apps.get_model("pages", "AboutPage")
    ServicesPage = apps.get_model("pages", "ServicesPage")
    ServiceItem = apps.get_model("pages", "ServiceItem")
    TherapyPage = apps.get_model("pages", "TherapyPage")
    TherapyStep = apps.get_model("pages", "TherapyStep")

    site = SiteSettings.objects.first()
    if site:
        site.brand_name_uk = BRAND_UK
        site.brand_name_it = BRAND_IT
        site.tagline_uk = TAGLINE_UK
        site.tagline_it = TAGLINE_IT
        site.save(update_fields=["brand_name_uk", "brand_name_it", "tagline_uk", "tagline_it"])

    home = HomePage.objects.first()
    if home:
        home.hero_title_uk = HERO_TITLE_UK
        home.hero_title_it = HERO_TITLE_IT
        home.hero_subtitle_uk = HERO_SUBTITLE_UK
        home.hero_subtitle_it = HERO_SUBTITLE_IT
        home.positioning_uk = POSITIONING_UK
        home.positioning_it = POSITIONING_IT
        home.save(
            update_fields=[
                "hero_title_uk",
                "hero_title_it",
                "hero_subtitle_uk",
                "hero_subtitle_it",
                "positioning_uk",
                "positioning_it",
            ]
        )

    about = AboutPage.objects.first()
    if about:
        about.lead_uk = ABOUT_LEAD_UK
        about.lead_it = ABOUT_LEAD_IT
        about.body_uk = ABOUT_BODY_UK
        about.body_it = ABOUT_BODY_IT
        about.education_uk = ABOUT_EDUCATION_UK
        about.education_it = ABOUT_EDUCATION_IT
        about.approach_uk = ABOUT_APPROACH_UK
        about.approach_it = ABOUT_APPROACH_IT
        about.save(
            update_fields=[
                "lead_uk",
                "lead_it",
                "body_uk",
                "body_it",
                "education_uk",
                "education_it",
                "approach_uk",
                "approach_it",
            ]
        )

    services = ServicesPage.objects.first()
    if services:
        services.title_uk = SERVICES_TITLE_UK
        services.title_it = SERVICES_TITLE_IT
        services.intro_uk = SERVICES_INTRO_UK
        services.intro_it = SERVICES_INTRO_IT
        services.outro_uk = SERVICES_OUTRO_UK
        services.outro_it = SERVICES_OUTRO_IT
        services.save(
            update_fields=[
                "title_uk",
                "title_it",
                "intro_uk",
                "intro_it",
                "outro_uk",
                "outro_it",
            ]
        )

        ServiceItem.objects.filter(page=services).delete()
        for i, (tuk, tit) in enumerate(zip(SERVICE_ITEMS_UK, SERVICE_ITEMS_IT)):
            ServiceItem.objects.create(
                page=services,
                order=i,
                title_uk=tuk,
                title_it=tit,
                description_uk="",
                description_it="",
            )

    therapy = TherapyPage.objects.first()
    if therapy:
        therapy.title_it = THERAPY_TITLE_IT
        therapy.intro_uk = THERAPY_INTRO_UK
        therapy.intro_it = THERAPY_INTRO_IT
        therapy.save(update_fields=["title_it", "intro_uk", "intro_it"])

        TherapyStep.objects.filter(page=therapy).delete()
        for order, (tuk, tik, buk, bik) in enumerate(STEPS_UK_IT, start=1):
            TherapyStep.objects.create(
                page=therapy,
                order=order,
                title_uk=tuk,
                title_it=tik,
                body_uk=buk,
                body_it=bik,
            )


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0006_alter_servicespage_options_alter_therapypage_options_and_more"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
        migrations.AlterField(
            model_name="servicespage",
            name="title_uk",
            field=models.CharField(
                default="З чим я працюю",
                max_length=200,
                verbose_name="Заголовок (UA)",
            ),
        ),
        migrations.AlterField(
            model_name="therapypage",
            name="title_it",
            field=models.CharField(
                default="Come procedono gli incontri",
                max_length=200,
                verbose_name="Заголовок (IT)",
            ),
        ),
    ]
