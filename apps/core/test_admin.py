from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminExperienceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = get_user_model().objects.create_superuser(
            username="site-admin",
            email="admin@example.com",
            password="test-password-only",
        )

    def test_admin_login_uses_branded_secure_template(self):
        response = self.client.get(reverse("admin:login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign in to the dashboard")
        self.assertContains(response, "Keep TIIH content accurate")
        self.assertContains(response, "Authorized access")
        self.assertNotContains(response, "autofocus")

    def test_authenticated_admin_lands_on_content_dashboard(self):
        self.client.force_login(self.superuser)

        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Content workspace")
        self.assertContains(response, "Website Content")
        self.assertContains(response, "Innovation Projects")
        self.assertContains(response, "Contact Enquiries")
        self.assertContains(response, "View live website")
