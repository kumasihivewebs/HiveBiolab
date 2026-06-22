from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth.models import Group

from .models import (
    PageContent,
    Project,
    ProjectUpload,
    TrainingProgram,
    TrainingProgramUpload,
)


try:
    admin.site.unregister(Group)
except NotRegistered:
    pass


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "updated_at")
    readonly_fields = ("updated_at",)
    fieldsets = (
        (None, {"fields": ("key", "title", "eyebrow", "description")}),
        (
            "Structured page data",
            {
                "fields": (
                    "stats",
                    "filters",
                    "application_steps",
                    "contact",
                    "inquiry_types",
                )
            },
        ),
        ("System", {"fields": ("updated_at",)}),
    )


class ProjectUploadInline(admin.TabularInline):
    model = ProjectUpload
    extra = 1
    fields = ("title", "file", "upload_type", "is_public")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = (ProjectUploadInline,)
    list_display = ("title", "status", "category", "is_published")
    list_editable = ("is_published",)
    list_filter = ("status", "category", "is_published")
    search_fields = ("title", "description", "long_description", "category")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "description",
                    "long_description",
                    "status",
                    "category",
                    "image",
                    "image_url",
                    "is_published",
                )
            },
        ),
        ("Structured details", {"fields": ("tags", "team", "collaborators", "impact", "gallery")}),
        ("Dates and funding", {"fields": ("start_date", "end_date", "funding")}),
        ("Links", {"fields": ("route", "github_url", "website_url", "publication_url")}),
        ("Legacy frontend mapping", {"fields": ("image_key",)}),
        ("System", {"fields": ("created_at", "updated_at")}),
    )


class TrainingProgramUploadInline(admin.TabularInline):
    model = TrainingProgramUpload
    extra = 1
    fields = ("title", "file", "upload_type", "is_public")


@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    inlines = (TrainingProgramUploadInline,)
    list_display = ("title", "level", "is_published")
    list_editable = ("is_published",)
    list_filter = ("level", "is_published")
    search_fields = ("title", "description", "overview", "curriculum")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "description",
                    "level",
                    "image",
                    "image_url",
                    "icon_name",
                    "route",
                    "is_published",
                )
            },
        ),
        (
            "Program details",
            {
                "fields": (
                    "overview",
                    "curriculum",
                    "prerequisites",
                    "outcomes",
                    "duration",
                    "format",
                    "certification",
                )
            },
        ),
        ("Frontend styling", {"fields": ("color", "image_key")}),
        ("System", {"fields": ("created_at", "updated_at")}),
    )
