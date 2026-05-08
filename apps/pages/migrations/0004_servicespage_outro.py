from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0003_update_therapy_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="servicespage",
            name="outro_uk",
            field=models.TextField("Закриваючий текст (UA)", blank=True, default=""),
        ),
        migrations.AddField(
            model_name="servicespage",
            name="outro_it",
            field=models.TextField("Закриваючий текст (IT)", blank=True, default=""),
        ),
    ]
