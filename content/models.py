from django.db import models
from django.utils import timezone


def list_default():
    return []


def dict_default():
    return {}


class PageContent(models.Model):
    class PageKey(models.TextChoices):
        PROJECTS = "projects", "Projects"
        TRAINING = "training", "Training"
        CONTACT = "contact", "Contact"

    key = models.CharField(max_length=64, choices=PageKey.choices, unique=True)
    title = models.CharField(max_length=255, blank=True)
    eyebrow = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    stats = models.JSONField(default=list_default, blank=True)
    filters = models.JSONField(default=list_default, blank=True)
    application_steps = models.JSONField(default=list_default, blank=True)
    contact = models.JSONField(default=dict_default, blank=True)
    inquiry_types = models.JSONField(default=list_default, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["key"]
        verbose_name = "page content"
        verbose_name_plural = "page content"

    def __str__(self):
        return self.get_key_display()


class Project(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "Active", "Active"
        COMPLETED = "Completed", "Completed"
        PLANNING = "Planning", "Planning"
        ON_HOLD = "On Hold", "On Hold"

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    long_description = models.TextField(blank=True)
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    category = models.CharField(max_length=255, blank=True)
    tags = models.JSONField(default=list_default, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to="projects/", max_length=500, blank=True)
    image_url = models.URLField(
        "image URL",
        max_length=1000,
        blank=True,
        help_text="Optional external image URL, for example a Cloudinary delivery URL.",
    )
    image_key = models.CharField(max_length=255, blank=True)
    gallery = models.JSONField(default=list_default, blank=True)
    team = models.JSONField(default=list_default, blank=True)
    collaborators = models.JSONField(default=list_default, blank=True)
    funding = models.CharField(max_length=255, blank=True)
    impact = models.JSONField(default=list_default, blank=True)
    route = models.CharField(max_length=255, blank=True)
    github_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    publication_url = models.URLField(blank=True)
    is_published = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "title"]

    def __str__(self):
        return self.title


class ProjectUpload(models.Model):
    class UploadType(models.TextChoices):
        IMAGE = "image", "Image"
        FLYER = "flyer", "Flyer"
        DOCUMENT = "document", "Document"
        OTHER = "other", "Other"

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="uploads",
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="projects/uploads/", max_length=500)
    upload_type = models.CharField(
        max_length=32,
        choices=UploadType.choices,
        default=UploadType.IMAGE,
    )
    is_public = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "title"]

    def __str__(self):
        return self.title


class TrainingProgram(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    level = models.CharField(max_length=255, blank=True)
    color = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="training-programs/", max_length=500, blank=True)
    image_url = models.URLField(
        "image URL",
        max_length=1000,
        blank=True,
        help_text="Optional external image URL, for example a Cloudinary delivery URL.",
    )
    image_key = models.CharField(max_length=255, blank=True)
    icon_name = models.CharField(max_length=255, blank=True)
    route = models.CharField(max_length=255, blank=True)
    overview = models.TextField(blank=True)
    curriculum = models.JSONField(default=list_default, blank=True)
    prerequisites = models.TextField(blank=True)
    outcomes = models.TextField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    registration_open = models.BooleanField(default=True)
    duration = models.CharField(max_length=255, blank=True)
    format = models.CharField(max_length=255, blank=True)
    certification = models.CharField(max_length=255, blank=True)
    is_published = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "title"]

    def __str__(self):
        return self.title

    @property
    def schedule_status(self):
        today = timezone.localdate()

        if self.end_date and self.end_date < today:
            return "past"
        if self.start_date and self.start_date > today:
            return "upcoming"
        return "ongoing"

    @property
    def accepting_registrations(self):
        return self.registration_open and self.schedule_status != "past"


class TrainingProgramUpload(models.Model):
    class UploadType(models.TextChoices):
        IMAGE = "image", "Image"
        FLYER = "flyer", "Flyer"
        DOCUMENT = "document", "Document"
        OTHER = "other", "Other"

    program = models.ForeignKey(
        TrainingProgram,
        on_delete=models.CASCADE,
        related_name="uploads",
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="training-programs/uploads/", max_length=500)
    upload_type = models.CharField(
        max_length=32,
        choices=UploadType.choices,
        default=UploadType.FLYER,
    )
    is_public = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "title"]

    def __str__(self):
        return self.title
