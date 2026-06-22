from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth.models import Group

from .models import (
    Project,
    ProjectUpload,
    TrainingProgram,
    TrainingProgramUpload,
)


try:
    admin.site.unregister(Group)
except NotRegistered:
    pass


class ProjectUploadInline(admin.TabularInline):
    model = ProjectUpload
    extra = 1
    fields = ("title", "file", "upload_type", "is_public", "sort_order")


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
            "Project",
            {
                "fields": (
                    "title",
                    "slug",
                    "description",
                    "status",
                    "category",
                    "image",
                    "sort_order",
                    "is_published",
                )
            },
        ),
        (
            "Details",
            {
                "fields": (
                    "long_description",
                    "tags",
                    "team",
                    "collaborators",
                    "impact",
                    "gallery",
                    "start_date",
                    "end_date",
                    "funding",
                )
            },
        ),
        (
            "Links",
            {
                "fields": (
                    "route",
                    "github_url",
                    "website_url",
                    "publication_url",
                )
            },
        ),
        ("System", {"fields": ("created_at", "updated_at")}),
    )


class TrainingProgramUploadInline(admin.TabularInline):
    model = TrainingProgramUpload
    extra = 1
    fields = ("title", "file", "upload_type", "is_public", "sort_order")


@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    inlines = (TrainingProgramUploadInline,)
    list_display = ("title", "level", "registration_open", "is_published")
    list_editable = ("is_published",)
    list_filter = ("level", "registration_open", "is_published")
    search_fields = ("title", "description", "overview", "curriculum")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Training Program",
            {
                "fields": (
                    "title",
                    "slug",
                    "description",
                    "level",
                    "image",
                    "icon_name",
                    "route",
                    "sort_order",
                    "is_published",
                )
            },
        ),
        (
            "Schedule",
            {
                "fields": (
                    "start_date",
                    "end_date",
                    "registration_open",
                )
            },
        ),
        (
            "Details",
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
        ("System", {"fields": ("created_at", "updated_at")}),
    )
