from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0008_cloudinary_fields_and_cleanup_legacy_urls"),
    ]

    operations = [
        migrations.AddField(
            model_name="trainingprogram",
            name="registration_url",
            field=models.URLField(blank=True, max_length=1000),
        ),
    ]
