from django.db import connections
from django.db.utils import DatabaseError
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .content_data import PROJECTS_DATA, TRAINING_PROGRAMS_DATA


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
    return JsonResponse({"projects": PROJECTS_DATA})


@require_GET
def list_training_programs(request):
    """Return the catalog of training programs we offer."""
    return JsonResponse({"programs": TRAINING_PROGRAMS_DATA})
