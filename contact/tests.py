import json

from django.test import Client, TestCase
from django.urls import reverse

from content.models import PageContent

from .models import ContactMessage


class ContactAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("contact_submit")
        PageContent.objects.create(
            key=PageContent.PageKey.CONTACT,
            title="Contact from admin",
            eyebrow="Reach us",
            description="Admin-managed contact page copy.",
            contact={"email": "biolab@example.com"},
            inquiry_types=["Training inquiry"],
        )

    def test_contact_page_content_success(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["page"]["title"], "Contact from admin")
        self.assertIn("contact", payload["page"])

    def test_submit_message_success(self):
        payload = {
            "name": "Ada Bio",
            "email": "ada@biolab.org",
            "subject": "Collab",
            "message": "Would love to partner on training.",
        }
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        message = ContactMessage.objects.get(email="ada@biolab.org")
        self.assertEqual(response.json().get("message_id"), message.pk)
        self.assertEqual(message.subject, "Collab")

    def test_submit_requires_message(self):
        payload = {"name": "No Msg", "email": "no@biolab.org", "message": ""}
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_submit_requires_valid_json(self):
        response = self.client.post(
            self.url, data="nonsense", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
