"""Replace raw URLs in approach text with [text](url) markdown links."""
from django.db import migrations

URL = (
    "https://www.psy.it/la-professione-psicologica/"
    "codice-deontologico-degli-psicologi-italiani/"
    "codice-deontologico-vigente/"
)

OLD_UK = (
    f"Я працюю відповідно до етичного кодексу італійських психологів {URL} який гарантує "
    "конфіденційність, повагу до людини та її контексту, а також відповідальність за межі "
    "власної компетенції й постійний професійний розвиток.\n\n"
    "Я працюю в когнітивно-конструктивістському підході, що зосереджується на тому, як людина "
    "формує своє бачення реальності та які значення надає власному досвіду.\n\n"
    "У роботі я також використовую майндфулнес і роботу з тілом — як спосіб повернутися до себе, "
    "краще відчути свій стан і поступово відновити внутрішню опору, навіть після складних "
    "життєвих періодів."
)

NEW_UK = (
    f"Я працюю відповідно до [етичного кодексу італійських психологів]({URL}) який гарантує "
    "конфіденційність, повагу до людини та її контексту, а також відповідальність за межі "
    "власної компетенції й постійний професійний розвиток.\n\n"
    "Я працюю в когнітивно-конструктивістському підході, що зосереджується на тому, як людина "
    "формує своє бачення реальності та які значення надає власному досвіду.\n\n"
    "У роботі я також використовую майндфулнес і роботу з тілом — як спосіб повернутися до себе, "
    "краще відчути свій стан і поступово відновити внутрішню опору, навіть після складних "
    "життєвих періодів."
)

OLD_IT = (
    f"Mi attengo al codice deontologico degli psicologi italiani ({URL}), che garantisce "
    "riservatezza, rispetto della persona e del suo contesto, responsabilità sui limiti di "
    "competenza e aggiornamento professionale continuo.\n\n"
    "Lavoro nell'approccio cognitivo-costruttivista, con attenzione a come la persona costruisce "
    "la realtà e attribuisce significato alla propria esperienza.\n\n"
    "Utilizzo anche mindfulness e il lavoro sul corpo — per tornare a sé, percepire meglio il "
    "proprio stato e gradualmente ritrovare un sostegno interno, anche dopo periodi difficili."
)

NEW_IT = (
    f"Mi attengo al [codice deontologico degli psicologi italiani]({URL}), che garantisce "
    "riservatezza, rispetto della persona e del suo contesto, responsabilità sui limiti di "
    "competenza e aggiornamento professionale continuo.\n\n"
    "Lavoro nell'approccio cognitivo-costruttivista, con attenzione a come la persona costruisce "
    "la realtà e attribuisce significato alla propria esperienza.\n\n"
    "Utilizzo anche mindfulness e il lavoro sul corpo — per tornare a sé, percepire meglio il "
    "proprio stato e gradualmente ritrovare un sostegno interno, anche dopo periodi difficili."
)


def forwards(apps, schema_editor):
    AboutPage = apps.get_model("pages", "AboutPage")
    page = AboutPage.objects.first()
    if not page:
        return
    page.approach_uk = NEW_UK
    page.approach_it = NEW_IT
    page.save(update_fields=["approach_uk", "approach_it"])


def backwards(apps, schema_editor):
    AboutPage = apps.get_model("pages", "AboutPage")
    page = AboutPage.objects.first()
    if not page:
        return
    page.approach_uk = OLD_UK
    page.approach_it = OLD_IT
    page.save(update_fields=["approach_uk", "approach_it"])


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0014_remove_homepage_dead_fields"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
