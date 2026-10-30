from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.test import TestCase
from django.urls import reverse


class ServicePageTests(TestCase):
    def test_services_page_displays_seven_official_services(self):
        response = self.client.get(reverse("services:list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["services"]), 7)
        self.assertContains(response, "Shared Infrastructure")
        self.assertContains(response, "Research and Development")

    def test_services_are_static_and_have_no_database_table(self):
        self.assertEqual(list(apps.get_app_config("services").get_models()), [])
        self.assertNotIn("services_service", connection.introspection.table_names())
        self.assertFalse(ContentType.objects.filter(app_label="services", model="service").exists())
