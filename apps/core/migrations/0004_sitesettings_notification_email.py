from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_uilabels_add_missing_labels"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="notification_email",
            field=models.EmailField(
                blank=True,
                default="",
                help_text=(
                    "Куди надсилати листи про нові запити на консультацію. "
                    "Якщо порожньо — використовується публічний Email вище."
                ),
                verbose_name="Email для сповіщень про запис",
            ),
        ),
    ]
