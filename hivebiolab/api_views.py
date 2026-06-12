from django.db import connections
from django.db.utils import DatabaseError
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .api_helpers import json_error
from .content_data import (
    PROJECTS_DATA,
    PROJECTS_PAGE_DATA,
    TRAINING_PAGE_DATA,
    TRAINING_PROGRAMS_DATA,
)


def _find_by_slug(items, slug):
    return next((item for item in items if item.get("slug") == slug), None)


@require_GET
def health_check(request):
    try:
        connections["default"].ensure_connection()
    except DatabaseError:
        return JsonResponse({"status": "degraded", "database": "unavailable"}, status=503)

    return JsonResponse({"status": "ok", "database": "ok"})


@require_GET
def list_projects(request):
    """Return the curated list of Hive Biolab projects."""
    return JsonResponse({"page": PROJECTS_PAGE_DATA, "projects": PROJECTS_DATA})


@require_GET
def retrieve_project(request, slug):
    """Return a single Hive Biolab project by slug."""
    project = _find_by_slug(PROJECTS_DATA, slug)
    if project is None:
        return json_error("Project not found.", status=404)

    return JsonResponse({"project": project})


@require_GET
def training_page(request):
    """Return the training page content and program catalog."""
    return JsonResponse(
        {"page": TRAINING_PAGE_DATA, "programs": TRAINING_PROGRAMS_DATA}
    )


@require_GET
def list_training_programs(request):
    """Return the catalog of training programs we offer."""
    return JsonResponse({"programs": TRAINING_PROGRAMS_DATA})


@require_GET
def retrieve_training_program(request, slug):
    """Return a single training program by slug."""
    program = _find_by_slug(TRAINING_PROGRAMS_DATA, slug)
    if program is None:
        return json_error("Training program not found.", status=404)

    return JsonResponse({"program": program})
