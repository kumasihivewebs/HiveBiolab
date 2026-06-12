import logging

from django.db import DatabaseError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from hivebiolab.api_helpers import (
    parse_json_body,
    json_error,
    json_success,
    get_client_metadata,
)
from hivebiolab.content_data import CONTACT_PAGE_DATA

from .models import ContactMessage

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def submit_message(request):
    if request.method == "GET":
        return JsonResponse({"page": CONTACT_PAGE_DATA})

    payload = parse_json_body(request)
    if payload is None:
        return json_error("Invalid JSON payload.")

    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip()
    message = (payload.get("message") or "").strip()

    if not name or not email or not message:
        return json_error("Name, email, and message are required.")

    metadata = get_client_metadata(request)
    subject = (payload.get("subject") or "").strip() or "General inquiry"
    organization = (payload.get("organization") or "").strip() or None

    try:
        entry = ContactMessage.objects.create(
            name=name,
            email=email.lower(),
            subject=subject,
            message=message,
            organization=organization,
            metadata=metadata,
        )
    except DatabaseError as exc:  # pragma: no cover - DB failure
        logger.exception("Failed to persist contact message.", exc_info=exc)
        return json_error(
            "Unable to submit the form right now. Please try again later.", status=500
        )

    return json_success(
        "Thanks for reaching out! We will respond as soon as possible.",
        status=201,
        extra={"message_id": entry.pk},
    )
