import json
from datetime import timedelta

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from content.models import TrainingProgram
from .models import TrainingRegistration


class TrainingAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("training_register")
        self.program = TrainingProgram.objects.create(
            title="Synthetic Biology",
            slug="synthetic-biology",
            description="Program for testing registrations.",
        )

    def test_register_participant_success(self):
        payload = {
            "full_name": "Bianca Lab",
            "email": "bianca@biolab.org",
            "program": "Synthetic Biology",
            "phone": "+233501234567",
        }
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        registration = TrainingRegistration.objects.get(email="bianca@biolab.org")
        self.assertEqual(response.json().get("registration_id"), registration.pk)

    def test_register_rejects_closed_or_past_program(self):
        self.program.end_date = timezone.localdate() - timedelta(days=1)
        self.program.save(update_fields=["end_date"])
        payload = {
            "full_name": "Bianca Lab",
            "email": "bianca@biolab.org",
            "program": "Synthetic Biology",
            "program_slug": "synthetic-biology",
        }
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(TrainingRegistration.objects.count(), 0)

    def test_register_requires_fields(self):
        payload = {"full_name": "", "email": "test@biolab.org", "program": ""}
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_register_requires_valid_json(self):
        response = self.client.post(
            self.url, data="bad", content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
