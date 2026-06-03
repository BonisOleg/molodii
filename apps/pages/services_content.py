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

LEGACY_CARD_TITLES = {
    "Тривога і панічні атаки",
    "Стосунки і розставання",
    "Втрата і горе",
    "Самооцінка і самокритика",
    "Вигорання і втома",
    "Адаптація після переїзду",
}


def services_items_are_stale(items) -> bool:
    item_list = list(items)
    if len(item_list) != len(SERVICE_ITEMS_UK):
        return True
    for item in item_list:
        if item.title_uk in LEGACY_CARD_TITLES:
            return True
        if item.description_uk or item.description_it:
            return True
    titles = [item.title_uk for item in item_list]
    return titles != SERVICE_ITEMS_UK
