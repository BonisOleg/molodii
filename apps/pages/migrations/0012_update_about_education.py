"""Update AboutPage education fields with detailed text and markdown link."""
from django.db import migrations

OLD_UK = (
    "Вища освіта в Україні та Італії. Зареєстрована в Ордені психологів Ломбардії. "
    "https://www.opl.it/psicologi/28919/Molodii-Tetiana"
)
OLD_IT = (
    "Laurea in Ucraina e in Italia. Iscritta all'Ordine degli Psicologi della Lombardia. "
    "https://www.opl.it/psicologi/28919/Molodii-Tetiana"
)

NEW_UK = (
    "Вища психологічна освіта в Україні (Тернопіль) та магістратура по соціальній психології в Італії (Мілан)\n"
    "[Зареєстрована в ордені психологів Ломбардії](https://www.opl.it/psicologi/28919/Molodii-Tetiana)\n"
    "Проходжу спеціалізацію в школі для психотерапевтів Nous в Мілані."
)
NEW_IT = (
    "Laurea triennale in psicologia in Ucraina (Ternopil) e magistrale in psicologia sociale in Italia (Milano)\n"
    "[Iscritta all'Ordine degli Psicologi della Lombardia](https://www.opl.it/psicologi/28919/Molodii-Tetiana)\n"
    "Sto completando la specializzazione in psicoterapia presso la scuola Nous di Milano."
)


def forwards(apps, schema_editor):
    AboutPage = apps.get_model("pages", "AboutPage")
    page = AboutPage.objects.first()
    if not page:
        return
    page.education_uk = NEW_UK
    page.education_it = NEW_IT
    page.save(update_fields=["education_uk", "education_it"])


def backwards(apps, schema_editor):
    AboutPage = apps.get_model("pages", "AboutPage")
    page = AboutPage.objects.first()
    if not page:
        return
    page.education_uk = OLD_UK
    page.education_it = OLD_IT
    page.save(update_fields=["education_uk", "education_it"])


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0011_update_therapy_it_content"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
