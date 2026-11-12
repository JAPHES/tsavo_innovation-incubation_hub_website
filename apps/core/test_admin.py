import time
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from tsavo_hub.security import trusted_client_ip


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

        self.assertRedirects(response, reverse("admin:index"), fetch_redirect_response=False)
        self.assertTrue(self.client.session.get_expire_at_browser_close())
        self.assertTrue(self.client.get(reverse("admin:index")).url.startswith(reverse("mfa:security_settings")))

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

        self.assertRedirects(response, reverse("admin:index"), fetch_redirect_response=False)
        self.assertFalse(self.client.session.get_expire_at_browser_close())
        self.assertEqual(self.client.session.get_expiry_age() // 3600, 8)

    def test_authenticated_admin_lands_on_content_dashboard(self):
        self.client.force_login(self.superuser)
        session = self.client.session
        session["mfa"] = {"verified": True, "method": "totp", "at": int(time.time())}
        session.save()

        with patch("django_mfa.registry.registry.has_primary_factor", return_value=True):
            response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Content workspace")
        self.assertContains(response, "Website Content")
        self.assertContains(response, "Innovation Projects")
        self.assertContains(response, "Contact Enquiries")
        self.assertContains(response, "View live website")

    def test_unenrolled_admin_is_sent_to_mfa_setup_and_can_sign_out(self):
        self.client.force_login(self.superuser)

        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("mfa:security_settings")))

        setup = self.client.get(reverse("mfa:security_settings"))
        self.assertContains(setup, "Two-factor authentication is required")
        self.assertContains(setup, reverse("admin_sign_out"))

        response = self.client.post(reverse("admin_sign_out"))
        self.assertRedirects(response, reverse("admin:login"))
        self.assertFalse(self.client.session.get("_auth_user_id"))

    def test_public_pages_have_a_stricter_csp_than_admin(self):
        public = self.client.get(reverse("core:home"))
        admin = self.client.get(reverse("admin:login"))

        self.assertIn("Content-Security-Policy", public)
        self.assertIn("script-src 'self' https://cdn.jsdelivr.net", public["Content-Security-Policy"])
        self.assertNotIn("'unsafe-inline'", public["Content-Security-Policy"].split("script-src ")[1].split(";")[0])
        self.assertIn("script-src 'self' 'unsafe-inline'", admin["Content-Security-Policy"])
        self.assertIn("no-store", admin["Cache-Control"])
        self.assertContains(public, 'integrity="sha384-')

    def test_repeated_admin_password_failures_are_rate_limited(self):
        login_url = reverse("admin:login")
        for _ in range(5):
            response = self.client.post(
                login_url,
                {"username": "site-admin", "password": "wrong-password"},
                HTTP_X_FORWARDED_FOR="198.51.100.20",
            )
        self.assertEqual(response.status_code, 429)

        response = self.client.post(
            login_url,
            {"username": "site-admin", "password": "test-password-only"},
            HTTP_X_FORWARDED_FOR="198.51.100.21",
        )
        self.assertEqual(response.status_code, 429)

    @override_settings(IS_VERCEL=True)
    def test_vercel_client_ip_uses_the_edge_overwritten_header(self):
        request = RequestFactory().get(
            "/admin/login/",
            HTTP_X_FORWARDED_FOR="198.51.100.20, 10.0.0.1",
            REMOTE_ADDR="10.0.0.2",
        )
        self.assertEqual(trusted_client_ip(request), "198.51.100.20")

    def test_local_client_ip_ignores_untrusted_forwarding_header(self):
        request = RequestFactory().get(
            "/admin/login/",
            HTTP_X_FORWARDED_FOR="198.51.100.20",
            REMOTE_ADDR="127.0.0.1",
        )
        self.assertEqual(trusted_client_ip(request), "127.0.0.1")
