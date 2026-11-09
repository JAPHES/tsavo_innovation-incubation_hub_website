from datetime import timedelta

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.contrib.staticfiles import finders
from django.core.management import call_command
from django.db import connection
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.events.models import Event


class CorePageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_initial_data", verbosity=0)

    def test_homepage_and_about_return_200(self):
        self.assertEqual(self.client.get(reverse("core:home")).status_code, 200)
        self.assertEqual(self.client.get(reverse("core:about")).status_code, 200)

    def test_homepage_section_order(self):
        html = self.client.get(reverse("core:home")).content.decode()
        section_ids = ["about-hub", "chair-message", "services", "innovations", "programs", "events"]
        positions = [html.index(f'id="{section_id}"') for section_id in section_ids]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn('id="highlights"', html)

    def test_homepage_requested_content_and_navigation_updates(self):
        html = self.client.get(reverse("core:home")).content.decode()
        self.assertIn("About TIIH", html)
        self.assertIn("What TIIH Does", html)
        self.assertIn("Dr. Mwakio Mwagandi", html)
        self.assertIn("Upcycled Cotton Hydro-Pellets", html)
        self.assertIn("AI-Powered Multilingual Learning Platform", html)
        self.assertIn("Blue Bin", html)
        self.assertIn("Innovation Pitch &amp; Partnership Forum", html)
        self.assertIn('class="section innovation-section" id="innovations"', html)
        self.assertNotIn('class="section dark-section" id="innovations"', html)
        self.assertNotIn("Draft event", html)
        self.assertLess(html.index("Blue Bin"), html.index("View all innovations"))
        self.assertNotIn("SolarSmart Irrigation Kit", html)
        self.assertNotIn("EcoBrick Circular Build Lab", html)
        self.assertNotIn("Jirani Market Link", html)
        self.assertNotIn("Temporary non-institutional image", html)
        self.assertNotIn('class="nav-contact', html)
        self.assertNotIn('class="brand" href=', html)

    def test_banner_static_fallback_renders(self):
        response = self.client.get(reverse("core:about"))
        self.assertContains(response, "images/banners/tiih_outreach_about.jpeg")
        self.assertContains(response, "Where Innovation Takes Root")
        self.assertNotContains(response, "TIIH: Where Innovation Takes Root")

        for route in ("core:home", "services:list", "projects:list", "team:list", "contact:contact"):
            with self.subTest(route=route):
                self.assertContains(self.client.get(reverse(route)), "images/banners/tiih_training_hero.png")

    def test_about_foundation_and_values_layout(self):
        html = self.client.get(reverse("core:about")).content.decode()
        self.assertIn('class="section pillars-section"', html)
        self.assertEqual(html.count('class="vision-card"'), 3)
        self.assertIn('<span class="eyebrow">Vision</span>', html)
        self.assertIn('<span class="eyebrow">Mission</span>', html)
        self.assertNotIn('<span class="eyebrow">Our vision</span>', html)
        self.assertNotIn('<span class="eyebrow">Our mission</span>', html)
        self.assertEqual(html.count('class="foundation-copy"'), 3)
        self.assertNotIn('<h3>A flourishing society powered by innovation and entrepreneurship</h3>', html)
        self.assertIn('class="section values-section"', html)
        self.assertNotIn('class="section dark-section"', html)

    def test_fixed_content_uses_no_database_tables(self):
        removed_models = ("ChairMessage", "CoreValue", "FocusArea", "Program", "Achievement")
        for model_name in removed_models:
            with self.assertRaises(LookupError):
                apps.get_model("core", model_name)

        table_names = connection.introspection.table_names()
        for table_name in (
            "core_chairmessage",
            "core_corevalue",
            "core_focusarea",
            "core_program",
            "core_achievement",
        ):
            self.assertNotIn(table_name, table_names)
        self.assertFalse(
            ContentType.objects.filter(
                app_label="core",
                model__in=("achievement", "chairmessage", "corevalue", "focusarea", "program"),
            ).exists()
        )

        home = self.client.get(reverse("core:home"))
        about = self.client.get(reverse("core:about"))
        self.assertContains(home, "Dr. Mwakio Mwagandi")
        self.assertContains(home, "Innovation Incubation")
        self.assertContains(about, "Innovativeness")
        self.assertContains(about, "Cross-cutting Areas")

    def test_upcoming_event_is_shown_and_past_event_is_hidden(self):
        Event.objects.create(title="Future approved event", slug="future-event", description="Future", venue="Online", start_datetime=timezone.now() + timedelta(days=3), is_published=True)
        Event.objects.create(title="Past approved event", slug="past-event", description="Past", venue="Online", start_datetime=timezone.now() - timedelta(days=3), is_published=True)
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "Future approved event")
        self.assertNotContains(response, "Past approved event")

    def test_required_static_assets_resolve(self):
        for asset in [
            "css/main.css",
            "js/main.js",
            "images/banners/tiih_training_hero.png",
            "images/banners/tiih_outreach_about.jpeg",
            "images/home/tiih_ideas_enterprise.png",
            "images/placeholders/project_default.jpg",
            "images/team/chair_dr_mwakio_mwagandi.jpg",
            "images/branding/tiih_logo_round.png",
            "images/innovations/upcycled-cotton-hydro-pellets.png",
            "images/innovations/multilingual-learning-platform.svg",
            "images/innovations/blue-bin-pwani-innovation-week.png",
        ]:
            self.assertIsNotNone(finders.find(asset), asset)

    def test_robots_and_sitemap_load(self):
        self.assertEqual(self.client.get(reverse("core:robots")).status_code, 200)
        self.assertEqual(self.client.get("/sitemap.xml").status_code, 200)
