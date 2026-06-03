"""Canonical Therapy page copy."""

THERAPY_TITLE_UK = "Як проходить робота"
THERAPY_TITLE_IT = "Come si svolge il lavoro"

THERAPY_PRICING_NOTE_UK = (
    "Сесія триває 50 хвилин. Регулярність — раз на тиждень. "
    "Вартість і деталі обговорюємо при знайомстві."
)
THERAPY_PRICING_NOTE_IT = (
    "La sessione dura 50 minuti. Frequenza — settimanale. "
    "Tariffe e dettagli li discutiamo alla conoscenza."
)

THERAPY_STEPS = [
    {
        "title_uk": "Призначаємо першу зустріч, де підписуємо інформовану згоду",
        "title_it": "Fissiamo il primo incontro, in cui firmiamo il consenso informato",
        "body_uk": "",
        "body_it": "",
    },
    {
        "title_uk": "На перших зустрічах окреслюємо запит і визначаємо цілі",
        "title_it": "Nei primi incontri delimitiamo la richiesta e definiamo gli obiettivi",
        "body_uk": "",
        "body_it": "",
    },
    {
        "title_uk": "Поступово формуємо процес, у якому рухаємось до змін",
        "title_it": "Gradualmente costruiamo un percorso in cui ci muoviamo verso il cambiamento",
        "body_uk": "",
        "body_it": "",
    },
    {
        "title_uk": "За потреби можливий формат разової консультації",
        "title_it": "Se necessario è possibile una consulenza singola",
        "body_uk": (
            "зустріч, на якій ви отримуєте моє професійне бачення ситуації та, "
            "якщо потрібно, рекомендації щодо подальшого звернення."
        ),
        "body_it": (
            "un incontro in cui ricevete una lettura professionale della situazione e, "
            "se necessario, indicazioni su come proseguire."
        ),
    },
]

LEGACY_STEP_TITLES = {
    "Знайомство",
    "Контракт",
    "Перші сесії",
    "Робота",
    "Завершення",
}


def therapy_steps_are_stale(steps) -> bool:
    step_list = list(steps)
    if len(step_list) != len(THERAPY_STEPS):
        return True
    if any(step.title_uk in LEGACY_STEP_TITLES for step in step_list):
        return True
    expected_titles = [step["title_uk"] for step in THERAPY_STEPS]
    actual_titles = [step.title_uk for step in step_list]
    return actual_titles != expected_titles
