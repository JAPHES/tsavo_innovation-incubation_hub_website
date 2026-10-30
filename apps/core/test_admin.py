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
        self.assertContains(response, "Admin Portal")
        self.assertContains(response, "Tsavo Innovation &amp; Incubation Hub")
        self.assertContains(response, "Authorized personnel only. All access is logged.")
        self.assertContains(response, 'name="remember_me"')
        self.assertNotContains(response, "autofocus")

    def test_admin_login_session_expires_with_browser_by_default(self):
        response = self.client.post(
            reverse("admin:login"),
            {"username": "site-admin", "password": "test-password-only", "next": reverse("admin:index")},
        )

        self.assertRedirects(response, reverse("admin:index"))
        self.assertTrue(self.client.session.get_expire_at_browser_close())

    def test_remember_me_uses_persistent_session(self):
        response = self.client.post(
            reverse("admin:login"),
            {
                "username": "site-admin",
                "password": "test-password-only",
                "remember_me": "on",
                "next": reverse("admin:index"),
            },
        )

        self.assertRedirects(response, reverse("admin:index"))
        self.assertFalse(self.client.session.get_expire_at_browser_close())

    def test_authenticated_admin_lands_on_content_dashboard(self):
        self.client.force_login(self.superuser)

        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Content workspace")
        self.assertContains(response, "Website Content")
        self.assertContains(response, "Innovation Projects")
        self.assertContains(response, "Contact Enquiries")
        self.assertContains(response, "View live website")
