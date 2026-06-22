from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from content.models import PageContent, Project, TrainingProgram


class HealthCheckTests(TestCase):
    def test_health_check_reports_ok(self):
        response = self.client.get(reverse("health_check"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "database": "ok"})


class PageContentAPITests(TestCase):
    def setUp(self):
        self.projects_page = PageContent.objects.create(
            key=PageContent.PageKey.PROJECTS,
            title="Projects from admin",
            eyebrow="Managed content",
            description="Admin-managed project page copy.",
            stats=[{"label": "Projects", "value": "1"}],
        )
        self.training_page = PageContent.objects.create(
            key=PageContent.PageKey.TRAINING,
            title="Training from admin",
            eyebrow="Managed training",
            description="Admin-managed training page copy.",
            stats=[{"label": "Tracks", "value": "1"}],
            application_steps=["Apply", "Confirm", "Attend"],
        )
        self.project = Project.objects.create(
            title="Admin Project",
            slug="admin-project",
            description="A project created through the admin.",
            status=Project.Status.ACTIVE,
            category="Open Science",
            route="/projects/admin-project",
        )
        self.program = TrainingProgram.objects.create(
            title="Admin Training Program",
            slug="admin-training-program",
            description="A training program created through the admin.",
            level="Beginner",
            route="/training/admin-training-program",
            curriculum=["Lab safety", "Practical session"],
            registration_open=True,
        )

    def test_projects_list_includes_page_content(self):
        response = self.client.get(reverse("projects_list"))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["page"]["title"], "Projects from admin")
        self.assertEqual(payload["projects"][0]["slug"], "admin-project")

    def test_project_detail_uses_slug(self):
        response = self.client.get(
            reverse("project_detail", kwargs={"slug": "admin-project"})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["project"]["id"], str(self.project.pk))

    def test_project_image_ignores_legacy_transformed_cloudinary_url(self):
        cloudinary_url = (
            "https://res.cloudinary.com/kumasihivewebsite/image/upload/"
            "f_auto,q_auto/projects/MG_0391_lxakcg"
        )
        self.project.image.name = cloudinary_url
        self.project.save(update_fields=["image"])

        response = self.client.get(
            reverse("project_detail", kwargs={"slug": "admin-project"})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["project"]["image"], "")

    def test_project_image_repairs_double_prefixed_cloudinary_url(self):
        cloudinary_url = (
            "https://res.cloudinary.com/kumasihivewebsite/image/upload/"
            "f_auto,q_auto/projects/MG_0391_lxakcg"
        )
        self.project.image.name = (
            "https://res.cloudinary.com/kumasihivewebsite/image/upload/"
            f"f_auto,q_auto/{cloudinary_url}"
        )
        self.project.save(update_fields=["image"])

        response = self.client.get(
            reverse("project_detail", kwargs={"slug": "admin-project"})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["project"]["image"], "")

    def test_project_image_url_repairs_pasted_cloudinary_delivery_url(self):
        self.project.image_url = (
            "https://res.cloudinary.com/kumasihivewebsite/image/upload/v1781390828/"
            "https:/res.cloudinary.com/kumasihivewebsite/image/upload/"
            "f_auto%2Cq_auto/projects/IMG_5612-scaled_jdvndj.jpg"
        )
        self.project.save(update_fields=["image_url"])

        response = self.client.get(
            reverse("project_detail", kwargs={"slug": "admin-project"})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["project"]["image"],
            (
                "https://res.cloudinary.com/kumasihivewebsite/image/upload/"
                "projects/IMG_5612-scaled_jdvndj.jpg"
            ),
        )

    def test_project_image_url_repairs_separately_pasted_transformed_url(self):
        self.project.image_url = (
            "https://res.cloudinary.com/kumasihivewebsite/image/upload/"
            "f_auto,q_auto/projects/IMG_5612-scaled_jdvndj.jpg"
        )
        self.project.save(update_fields=["image_url"])

        response = self.client.get(
            reverse("project_detail", kwargs={"slug": "admin-project"})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["project"]["image"],
            (
                "https://res.cloudinary.com/kumasihivewebsite/image/upload/"
                "projects/IMG_5612-scaled_jdvndj.jpg"
            ),
        )

    def test_project_image_field_takes_priority_over_legacy_image_url(self):
        self.project.image.name = "projects/IMG_5612-scaled_jdvndj"
        self.project.image_url = (
            "https://res.cloudinary.com/kumasihivewebsite/image/upload/"
            "https:/res.cloudinary.com/kumasihivewebsite/image/upload/"
            "f_auto%2Cq_auto/projects/bad_legacy_value.jpg"
        )
        self.project.save(update_fields=["image", "image_url"])

        response = self.client.get(
            reverse("project_detail", kwargs={"slug": "admin-project"})
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "projects/IMG_5612-scaled_jdvndj",
            response.json()["project"]["image"],
        )

    def test_unknown_project_returns_404(self):
        response = self.client.get(
            reverse("project_detail", kwargs={"slug": "missing-project"})
        )

        self.assertEqual(response.status_code, 404)

    def test_training_page_includes_program_catalog(self):
        response = self.client.get(reverse("training_page"))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["page"]["title"], "Training from admin")
        self.assertEqual(payload["programs"][0]["slug"], "admin-training-program")

    def test_training_program_detail_uses_slug(self):
        response = self.client.get(
            reverse(
                "training_program_detail",
                kwargs={"slug": "admin-training-program"},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["program"]["id"], str(self.program.pk))

    def test_training_program_detail_includes_schedule_state(self):
        self.program.start_date = timezone.localdate()
        self.program.end_date = timezone.localdate()
        self.program.registration_open = False
        self.program.save(update_fields=["start_date", "end_date", "registration_open"])

        response = self.client.get(
            reverse(
                "training_program_detail",
                kwargs={"slug": "admin-training-program"},
            )
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()["program"]
        self.assertEqual(payload["registrationStatus"], "ongoing")
        self.assertFalse(payload["registrationOpen"])
        self.assertFalse(payload["acceptingRegistrations"])

    def test_training_program_image_field_takes_priority_over_legacy_image_url(self):
        self.program.image.name = "training-programs/program-image"
        self.program.image_url = (
            "https://res.cloudinary.com/kumasihivewebsite/image/upload/"
            "https:/res.cloudinary.com/kumasihivewebsite/image/upload/"
            "f_auto%2Cq_auto/training-programs/bad_legacy_value.jpg"
        )
        self.program.save(update_fields=["image", "image_url"])

        response = self.client.get(
            reverse(
                "training_program_detail",
                kwargs={"slug": "admin-training-program"},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "training-programs/program-image",
            response.json()["program"]["image"],
        )

    def test_unknown_training_program_returns_404(self):
        response = self.client.get(
            reverse("training_program_detail", kwargs={"slug": "missing-program"})
        )

        self.assertEqual(response.status_code, 404)
