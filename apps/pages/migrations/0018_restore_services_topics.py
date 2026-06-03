"""Restore editorial Services topics after bullet-list migration 0017."""
from django.db import migrations

from apps.pages.services_content import (
    SERVICES_INTRO_IT,
    SERVICES_INTRO_UK,
    SERVICES_OUTRO_IT,
    SERVICES_OUTRO_UK,
)

# Snapshot for historical runs — do not import live services_content tuples.
_LEGACY_SERVICE_TOPICS = [
    (
        "Тривога і панічні атаки",
        "Ansia e attacchi di panico",
        "Як повернути контакт із собою, коли тіло «вмикає» тривогу.",
        "Come ritrovare il contatto con sé quando il corpo 'accende' l'ansia.",
    ),
    (
        "Стосунки і розставання",
        "Relazioni e separazioni",
        "Конфлікти, межі, втрата близькості, рішення «залишитись чи піти».",
        "Conflitti, confini, perdita di intimità, decisione 'restare o andare'.",
    ),
    (
        "Втрата і горе",
        "Perdita e lutto",
        "Простір прожити втрату — близької людини, дому, попереднього життя.",
        "Uno spazio per attraversare la perdita — di una persona cara, di una casa, della vita precedente.",
    ),
    (
        "Самооцінка і самокритика",
        "Autostima e autocritica",
        "Чому «я недостатньо хороший» — і як з цим вчитися інакше.",
        "Perché 'non sono abbastanza' — e come imparare diversamente.",
    ),
    (
        "Вигорання і втома",
        "Burnout e stanchezza",
        "Коли робота й піклування витискають усе. Робота з ресурсом.",
        "Quando lavoro e cura prosciugano tutto. Lavoro sulla risorsa.",
    ),
    (
        "Адаптація після переїзду",
        "Adattamento dopo la migrazione",
        "Ідентичність, мова, самотність, «ні там, ні тут».",
        "Identità, lingua, solitudine, 'né qui né là'.",
    ),
]

_BULLET_SERVICE_TITLES_UK = [
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


def _legacy_items_are_stale(items) -> bool:
    item_list = list(items)
    if len(item_list) != len(_LEGACY_SERVICE_TOPICS):
        return True
    for item, (title_uk, title_it, desc_uk, desc_it) in zip(item_list, _LEGACY_SERVICE_TOPICS):
        if item.title_uk != title_uk or item.title_it != title_it:
            return True
        if item.description_uk != desc_uk or item.description_it != desc_it:
            return True
    return False


def _items_are_bullet_list(items) -> bool:
    titles = [item.title_uk for item in items]
    return titles == _BULLET_SERVICE_TITLES_UK


def _sync_topics(ServiceItem, page):
    ServiceItem.objects.filter(page=page).delete()
    for i, (title_uk, title_it, desc_uk, desc_it) in enumerate(_LEGACY_SERVICE_TOPICS):
        ServiceItem.objects.create(
            page=page,
            order=i,
            title_uk=title_uk,
            title_it=title_it,
            description_uk=desc_uk,
            description_it=desc_it,
        )


def forwards(apps, schema_editor):
    ServicesPage = apps.get_model("pages", "ServicesPage")
    ServiceItem = apps.get_model("pages", "ServiceItem")

    page = ServicesPage.objects.first()
    if not page:
        return

    items = ServiceItem.objects.filter(page=page).order_by("order", "id")
    if not _legacy_items_are_stale(items) and not _items_are_bullet_list(items):
        return

    page.intro_uk = SERVICES_INTRO_UK
    page.intro_it = SERVICES_INTRO_IT
    page.outro_uk = SERVICES_OUTRO_UK
    page.outro_it = SERVICES_OUTRO_IT
    page.save(update_fields=["intro_uk", "intro_it", "outro_uk", "outro_it"])
    _sync_topics(ServiceItem, page)


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0017_repair_services_content"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
