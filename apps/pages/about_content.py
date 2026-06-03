"""Canonical About page copy with inline markdown links."""

OPL_URL = "https://www.opl.it/psicologi/28919/Molodii-Tetiana"
PSY_URL = (
    "https://www.psy.it/la-professione-psicologica/"
    "codice-deontologico-degli-psicologi-italiani/"
    "codice-deontologico-vigente/"
)

EDUCATION_UK = (
    "Вища психологічна освіта в Україні (Тернопіль) та магістратура по соціальній психології в Італії (Мілан)\n"
    f"[Зареєстрована в ордені психологів Ломбардії]({OPL_URL})\n"
    "Проходжу спеціалізацію в школі для психотерапевтів Nous в Мілані."
)
EDUCATION_IT = (
    "Laurea triennale in psicologia in Ucraina (Ternopil) e magistrale in psicologia sociale in Italia (Milano)\n"
    f"[Iscritta all'Ordine degli Psicologi della Lombardia]({OPL_URL})\n"
    "Sto completando la specializzazione in psicoterapia presso la scuola Nous di Milano."
)

APPROACH_UK = (
    f"Я працюю відповідно до [етичного кодексу італійських психологів]({PSY_URL}) який гарантує "
    "конфіденційність, повагу до людини та її контексту, а також відповідальність за межі "
    "власної компетенції й постійний професійний розвиток.\n\n"
    "Я працюю в когнітивно-конструктивістському підході, що зосереджується на тому, як людина "
    "формує своє бачення реальності та які значення надає власному досвіду.\n\n"
    "У роботі я також використовую майндфулнес і роботу з тілом — як спосіб повернутися до себе, "
    "краще відчути свій стан і поступово відновити внутрішню опору, навіть після складних "
    "життєвих періодів."
)
APPROACH_IT = (
    f"Mi attengo al [codice deontologico degli psicologi italiani]({PSY_URL}), che garantisce "
    "riservatezza, rispetto della persona e del suo contesto, responsabilità sui limiti di "
    "competenza e aggiornamento professionale continuo.\n\n"
    "Lavoro nell'approccio cognitivo-costruttivista, con attenzione a come la persona costruisce "
    "la realtà e attribuisce significato alla propria esperienza.\n\n"
    "Utilizzo anche mindfulness e il lavoro sul corpo — per tornare a sé, percepire meglio il "
    "proprio stato e gradualmente ritrovare un sostegno interno, anche dopo periodi difficili."
)


def education_has_raw_url(text: str) -> bool:
    return OPL_URL in text and f"]({OPL_URL})" not in text


def approach_has_raw_url(text: str) -> bool:
    return PSY_URL in text and f"]({PSY_URL})" not in text
