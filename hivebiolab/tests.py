from django.test import TestCase
from django.urls import reverse


class HealthCheckTests(TestCase):
    def test_health_check_reports_ok(self):
        response = self.client.get(reverse("health_check"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "database": "ok"})


class PageContentAPITests(TestCase):
    def test_projects_list_includes_page_content(self):
        response = self.client.get(reverse("projects_list"))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["page"]["title"], "Projects")
        self.assertGreaterEqual(len(payload["projects"]), 1)

    def test_project_detail_uses_slug(self):
        response = self.client.get(
            reverse("project_detail", kwargs={"slug": "ecb4osh-project"})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["project"]["id"], "ecb4osh")

    def test_unknown_project_returns_404(self):
        response = self.client.get(
            reverse("project_detail", kwargs={"slug": "missing-project"})
        )

        self.assertEqual(response.status_code, 404)

    def test_training_page_includes_program_catalog(self):
        response = self.client.get(reverse("training_page"))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["page"]["title"], "Training")
        self.assertGreaterEqual(len(payload["programs"]), 1)

    def test_training_program_detail_uses_slug(self):
        response = self.client.get(
            reverse(
                "training_program_detail",
                kwargs={"slug": "molecular-biology"},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["program"]["id"], "training-molecular-biology"
        )

    def test_unknown_training_program_returns_404(self):
        response = self.client.get(
            reverse("training_program_detail", kwargs={"slug": "missing-program"})
        )

        self.assertEqual(response.status_code, 404)
