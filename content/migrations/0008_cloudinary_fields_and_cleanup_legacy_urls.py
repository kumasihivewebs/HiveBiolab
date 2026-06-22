import cloudinary.models
from django.db import migrations


def clear_broken_legacy_image_urls(apps, schema_editor):
    def should_clear(image_value, image_url):
        if not image_value or not image_url:
            return False

        normalized = str(image_url)
        return (
            "https:/res.cloudinary.com/" in normalized
            or normalized.count("https://res.cloudinary.com/") > 1
            or normalized.count("http://res.cloudinary.com/") > 1
        )

    Project = apps.get_model("content", "Project")
    TrainingProgram = apps.get_model("content", "TrainingProgram")

    for model in (Project, TrainingProgram):
        for obj in model.objects.exclude(image_url="").iterator():
            if should_clear(getattr(obj, "image", None), obj.image_url):
                obj.image_url = ""
                obj.save(update_fields=["image_url"])


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0007_trainingprogram_schedule_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="image",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="image"
            ),
        ),
        migrations.AlterField(
            model_name="projectupload",
            name="file",
            field=cloudinary.models.CloudinaryField(
                blank=True,
                max_length=255,
                null=True,
                resource_type="auto",
                verbose_name="file",
            ),
        ),
        migrations.AlterField(
            model_name="trainingprogram",
            name="image",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="image"
            ),
        ),
        migrations.AlterField(
            model_name="trainingprogramupload",
            name="file",
            field=cloudinary.models.CloudinaryField(
                blank=True,
                max_length=255,
                null=True,
                resource_type="auto",
                verbose_name="file",
            ),
        ),
        migrations.RunPython(
            clear_broken_legacy_image_urls, migrations.RunPython.noop
        ),
    ]
