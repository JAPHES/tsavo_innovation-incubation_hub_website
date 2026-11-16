from datetime import timedelta
from io import BytesIO
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.password_validation import validate_password
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.events.models import Event
from apps.projects.models import InnovationProject
from PIL import Image
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

    def test_mfa_route_is_no_longer_available(self):
        self.assertEqual(self.client.get("/mfa/security/").status_code, 404)

    def test_admin_login_session_expires_with_browser_by_default(self):
        response = self.client.post(
            reverse("admin:login"),
            {"username": "site-admin", "password": "test-password-only", "next": reverse("admin:index")},
        )

        self.assertRedirects(response, reverse("admin:index"), fetch_redirect_response=False)
        self.assertTrue(self.client.session.get_expire_at_browser_close())
        self.assertContains(self.client.get(reverse("admin:index")), "Your publishing desk")

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
        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Innovation projects")
        self.assertContains(response, "Upcoming events")
        self.assertContains(response, reverse("admin:projects_innovationproject_add"))
        self.assertContains(response, reverse("admin:events_event_add"))
        self.assertContains(response, reverse("admin:projects_innovationproject_changelist"))
        self.assertContains(response, reverse("admin:events_event_changelist"))
        self.assertContains(response, "View live website")
        self.assertNotContains(response, "Two-factor security")
        self.assertNotContains(response, "Contact Enquiries")

    def test_project_and_event_upload_forms_are_available(self):
        self.client.force_login(self.superuser)
        project_form = self.client.get(reverse("admin:projects_innovationproject_add"))
        event_form = self.client.get(reverse("admin:events_event_add"))
        self.assertContains(project_form, 'name="cover_image"')
        self.assertContains(project_form, 'name="is_published"')
        self.assertContains(event_form, 'name="image"')
        self.assertContains(event_form, "No image uploaded")
        self.assertContains(event_form, 'name="start_datetime_0"')
        self.assertContains(event_form, "Only published events with a future start time appear on the homepage.")

    def test_admin_can_publish_a_project_and_upcoming_event(self):
        self.client.force_login(self.superuser)
        project_response = self.client.post(
            reverse("admin:projects_innovationproject_add"),
            {
                "title": "Test innovation project",
                "slug": "test-innovation-project",
                "short_description": "An approved innovation project.",
                "full_description": "Project details for publication.",
                "category": "agriculture",
                "development_stage": "idea",
                "homepage_order": "100",
                "is_published": "on",
                "gallery-TOTAL_FORMS": "0",
                "gallery-INITIAL_FORMS": "0",
                "gallery-MIN_NUM_FORMS": "0",
                "gallery-MAX_NUM_FORMS": "1000",
                "_save": "Save",
            },
        )
        errors = project_response.context["adminform"].form.errors if project_response.status_code == 200 else None
        self.assertEqual(project_response.status_code, 302, errors)
        self.assertTrue(InnovationProject.objects.filter(slug="test-innovation-project", is_published=True).exists())
        self.assertContains(self.client.get(reverse("projects:list")), "Test innovation project")

        future_date = timezone.localtime(timezone.now() + timedelta(days=30)).date()
        event_response = self.client.post(
            reverse("admin:events_event_add"),
            {
                "title": "Test upcoming workshop",
                "slug": "test-upcoming-workshop",
                "description": "An upcoming workshop for innovators.",
                "venue": "Taita Taveta University",
                "start_datetime_0": future_date.isoformat(),
                "start_datetime_1": "10:00:00",
                "is_published": "on",
                "_save": "Save",
            },
        )
        self.assertEqual(event_response.status_code, 302, event_response.content.decode()[:500])
        self.assertTrue(Event.objects.filter(slug="test-upcoming-workshop", is_published=True).exists())
        self.assertContains(self.client.get(reverse("core:home")), "Test upcoming workshop")

    def test_admin_can_upload_an_innovation_cover(self):
        self.client.force_login(self.superuser)
        image_bytes = BytesIO()
        Image.new("RGB", (12, 12), "green").save(image_bytes, format="PNG")
        upload = SimpleUploadedFile("approved-project.png", image_bytes.getvalue(), content_type="image/png")

        with TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            response = self.client.post(
                reverse("admin:projects_innovationproject_add"),
                {
                    "title": "Project with an approved image",
                    "slug": "project-with-approved-image",
                    "short_description": "A project with an uploaded cover.",
                    "full_description": "Approved project details.",
                    "homepage_order": "100",
                    "cover_image": upload,
                    "gallery-TOTAL_FORMS": "0",
                    "gallery-INITIAL_FORMS": "0",
                    "gallery-MIN_NUM_FORMS": "0",
                    "gallery-MAX_NUM_FORMS": "1000",
                    "_save": "Save",
                },
            )
            errors = response.context["adminform"].form.errors if response.status_code == 200 else None
            self.assertEqual(response.status_code, 302, errors)
            project = InnovationProject.objects.get(slug="project-with-approved-image")
            self.assertTrue(project.cover_image.storage.exists(project.cover_image.name))

    def test_dashboard_hides_actions_without_model_permissions(self):
        staff = get_user_model().objects.create_user(username="limited-staff", password="long-password-only", is_staff=True)
        self.client.force_login(staff)
        response = self.client.get(reverse("admin:index"))
        self.assertContains(response, "Project access has not been assigned")
        self.assertContains(response, "Event access has not been assigned")
        self.assertNotContains(response, reverse("admin:projects_innovationproject_add"))
        self.assertNotContains(response, reverse("admin:events_event_add"))

    def test_new_admin_passwords_require_twelve_characters(self):
        with self.assertRaises(ValidationError):
            validate_password("short123", self.superuser)

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
