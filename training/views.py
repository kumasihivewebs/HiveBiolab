import logging

from django.db import DatabaseError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from hivebiolab.api_helpers import (
    parse_json_body,
    json_error,
    json_success,
    get_client_metadata,
)

from content.models import TrainingProgram
from .models import TrainingRegistration

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def register_participant(request):
    payload = parse_json_body(request)
    if payload is None:
        return json_error("Invalid JSON payload.")

    full_name = (payload.get("full_name") or "").strip()
    email = (payload.get("email") or "").strip()
    program = (payload.get("program") or "").strip()
    program_slug = (payload.get("program_slug") or "").strip()

    if not full_name or not email or not program:
        return json_error("Full name, email, and program choice are required.")

    selected_program = None
    if program_slug:
        selected_program = TrainingProgram.objects.filter(
            slug=program_slug,
            is_published=True,
        ).first()
    else:
        selected_program = TrainingProgram.objects.filter(
            title=program,
            is_published=True,
        ).first()

    if selected_program and not selected_program.accepting_registrations:
        return json_error(
            "Registrations for this training program are currently closed.",
            status=400,
        )

    metadata = get_client_metadata(request)

    phone = (payload.get("phone") or "").strip()
    current_level = (payload.get("current_level") or "").strip() or None
    experience = (payload.get("experience") or "").strip() or None
    goals = (payload.get("goals") or "").strip() or None
    message = (payload.get("message") or "").strip() or None

    try:
        registration = TrainingRegistration.objects.create(
            full_name=full_name,
            email=email.lower(),
            phone=phone,
            program=program,
            current_level=current_level,
            experience_summary=experience,
            goals=goals,
            message=message,
            metadata=metadata,
        )
    except DatabaseError as exc:  # pragma: no cover - DB failure
        logger.exception("Failed to persist training registration.", exc_info=exc)
        return json_error(
            "Registration failed. Please try again later.", status=500
        )

    return json_success(
        "Registration received. Our team will reach out with next steps.",
        status=201,
        extra={"registration_id": registration.pk},
    )
