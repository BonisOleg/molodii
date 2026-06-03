"""Canonical Services page copy."""

SERVICES_INTRO_UK = "Ви можете звернутися до мене, якщо відчуваєте:"
SERVICES_INTRO_IT = "Puoi rivolgerti a me se provi:"

SERVICES_OUTRO_UK = (
    "Не потрібно бути в критичному стані, щоб звернутися до мене, "
    "Іноді достатньо відчути, що звичні способи більше не працюють і дати собі "
    "час та простір поступово знайти нові.\n\n"
    "Напишіть мені для того щоб дізнатись вартість зустрічей."
)
SERVICES_OUTRO_IT = (
    "Non è necessario trovarsi in una condizione critica per contattarmi. "
    "A volte basta accorgersi che le abituali strategie non funzionano più e concedersi "
    "tempo e spazio per trovarne di nuove, gradualmente.\n\n"
    "Scrivimi per conoscere le tariffe degli incontri."
)

# (title_uk, title_it, description_uk, description_it)
SERVICE_TOPICS = [
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

# Bullet-list copy replaced by migration 0017 — used to detect stale prod data.
# Kept for migration 0017 imports on fresh installs.
SERVICE_ITEMS_UK = BULLET_SERVICE_TITLES_UK = [
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


def services_items_are_stale(items) -> bool:
    item_list = list(items)
    if len(item_list) != len(SERVICE_TOPICS):
        return True
    for item, (title_uk, title_it, desc_uk, desc_it) in zip(item_list, SERVICE_TOPICS):
        if item.title_uk != title_uk or item.title_it != title_it:
            return True
        if item.description_uk != desc_uk or item.description_it != desc_it:
            return True
    return False


def services_items_are_bullet_list(items) -> bool:
    """True when DB still has the short-lived bullet-list seed from migration 0017."""
    titles = [item.title_uk for item in items]
    return titles == BULLET_SERVICE_TITLES_UK
