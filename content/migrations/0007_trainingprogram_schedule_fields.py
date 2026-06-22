from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0006_project_image_url_trainingprogram_image_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="trainingprogram",
            name="end_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="trainingprogram",
            name="registration_open",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="trainingprogram",
            name="start_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
