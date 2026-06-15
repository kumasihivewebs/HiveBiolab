from urllib.parse import unquote, urlsplit, urlunsplit

from django.db import connections
from django.db.utils import DatabaseError
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from content.models import PageContent, Project, TrainingProgram

from .api_helpers import json_error


def _normalized_absolute_file_url(value):
    value = str(value or "").strip()
    if not value:
        return ""

    value = unquote(value)

    for marker in (
        "https:/res.cloudinary.com/",
        "http:/res.cloudinary.com/",
        "https://res.cloudinary.com/",
        "http://res.cloudinary.com/",
    ):
        index = value.rfind(marker)
        if index > 0:
            value = value[index:]
            break

    value = value.replace("https:/res.cloudinary.com/", "https://res.cloudinary.com/")
    value = value.replace("http:/res.cloudinary.com/", "http://res.cloudinary.com/")

    if not value.startswith(("http://", "https://")):
        return ""

    parsed = urlsplit(value)
    if parsed.netloc == "res.cloudinary.com":
        path = parsed.path
        path = path.replace("/image/upload/f_auto,q_auto/", "/image/upload/")
        path = path.replace("/image/upload/q_auto,f_auto/", "/image/upload/")
        path = path.replace("/image/upload/f_auto,q_auto/", "/image/upload/")
        path = path.replace("/image/upload/q_auto,f_auto/", "/image/upload/")
        value = urlunsplit(parsed._replace(path=path))

    return value


def _file_url(request, file_field):
    if not file_field:
        return ""

    absolute_name_url = _normalized_absolute_file_url(
        getattr(file_field, "name", "")
    )
    if absolute_name_url:
        return absolute_name_url

    try:
        url = file_field.url
    except ValueError:
        return ""

    absolute_url = _normalized_absolute_file_url(url)
    if absolute_url:
        return absolute_url

    return request.build_absolute_uri(url)


def _legacy_transformed_cloudinary_url(value):
    parsed = urlsplit(unquote(str(value or "")))
    return (
        parsed.netloc == "res.cloudinary.com"
        and (
            "/image/upload/f_auto,q_auto/" in parsed.path
            or "/image/upload/q_auto,f_auto/" in parsed.path
        )
    )


def _public_file_url(request, file_field):
    if not file_field:
        return ""

    stored_name = getattr(file_field, "name", "")
    if _legacy_transformed_cloudinary_url(stored_name):
        return ""

    return _file_url(request, file_field)


def _image_url(request, external_url, file_field):
    normalized_external_url = _normalized_absolute_file_url(external_url)
    if normalized_external_url:
        return normalized_external_url

    return _public_file_url(request, file_field)


def _uploads_payload(request, uploads):
    return [
        {
            "title": upload.title,
            "url": _file_url(request, upload.file),
            "type": upload.upload_type,
        }
        for upload in uploads
        if upload.is_public
    ]


def _page_payload(key):
    page = PageContent.objects.filter(key=key).first()
    if page is None:
        return {}

    payload = {
        "title": page.title,
        "eyebrow": page.eyebrow,
        "description": page.description,
    }

    if page.stats:
        payload["stats"] = page.stats
    if page.filters:
        payload["filters"] = page.filters
    if page.application_steps:
        payload["applicationSteps"] = page.application_steps
    if page.contact:
        payload["contact"] = page.contact
    if page.inquiry_types:
        payload["inquiryTypes"] = page.inquiry_types

    return payload


def _project_payload(request, project):
    links = {
        key: value
        for key, value in {
            "github": project.github_url,
            "website": project.website_url,
            "publication": project.publication_url,
        }.items()
        if value
    }

    payload = {
        "id": str(project.pk),
        "title": project.title,
        "slug": project.slug,
        "description": project.description,
        "longDescription": project.long_description,
        "status": project.status,
        "category": project.category,
        "tags": project.tags,
        "startDate": project.start_date.isoformat() if project.start_date else "",
        "endDate": project.end_date.isoformat() if project.end_date else "",
        "image": _image_url(request, project.image_url, project.image),
        "image_url": _image_url(request, project.image_url, project.image),
        "image_key": project.image_key,
        "uploads": _uploads_payload(request, project.uploads.all()),
        "gallery": project.gallery,
        "team": project.team,
        "collaborators": project.collaborators,
        "funding": project.funding,
        "impact": project.impact,
        "route": project.route,
        "links": links,
    }
    return payload


def _training_program_payload(request, program):
    return {
        "id": str(program.pk),
        "slug": program.slug,
        "title": program.title,
        "description": program.description,
        "level": program.level,
        "color": program.color,
        "image": _image_url(request, program.image_url, program.image),
        "image_url": _image_url(request, program.image_url, program.image),
        "image_key": program.image_key,
        "uploads": _uploads_payload(request, program.uploads.all()),
        "icon_name": program.icon_name,
        "route": program.route,
        "details": {
            "overview": program.overview,
            "curriculum": program.curriculum,
            "prerequisites": program.prerequisites,
            "outcomes": program.outcomes,
            "duration": program.duration,
            "format": program.format,
            "certification": program.certification,
        },
    }


@require_GET
def health_check(request):
    try:
        connections["default"].ensure_connection()
    except DatabaseError:
        return JsonResponse({"status": "degraded", "database": "unavailable"}, status=503)

    return JsonResponse({"status": "ok", "database": "ok"})


@require_GET
def list_projects(request):
    """Return admin-managed Hive Biolab projects."""
    projects = Project.objects.filter(is_published=True)
    return JsonResponse(
        {
            "page": _page_payload(PageContent.PageKey.PROJECTS),
            "projects": [_project_payload(request, project) for project in projects],
        }
    )


@require_GET
def retrieve_project(request, slug):
    """Return a single admin-managed Hive Biolab project by slug."""
    try:
        project = Project.objects.get(slug=slug, is_published=True)
    except Project.DoesNotExist:
        return json_error("Project not found.", status=404)

    return JsonResponse({"project": _project_payload(request, project)})


@require_GET
def training_page(request):
    """Return admin-managed training page content and program catalog."""
    programs = TrainingProgram.objects.filter(is_published=True)
    return JsonResponse(
        {
            "page": _page_payload(PageContent.PageKey.TRAINING),
            "programs": [
                _training_program_payload(request, program) for program in programs
            ],
        }
    )


@require_GET
def list_training_programs(request):
    """Return admin-managed training programs."""
    programs = TrainingProgram.objects.filter(is_published=True)
    return JsonResponse(
        {
            "programs": [
                _training_program_payload(request, program) for program in programs
            ]
        }
    )


@require_GET
def retrieve_training_program(request, slug):
    """Return a single admin-managed training program by slug."""
    try:
        program = TrainingProgram.objects.get(slug=slug, is_published=True)
    except TrainingProgram.DoesNotExist:
        return json_error("Training program not found.", status=404)

    return JsonResponse({"program": _training_program_payload(request, program)})
