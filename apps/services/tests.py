from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Service


class ServicePageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_initial_data", verbosity=0)
        Service.objects.create(name="Hidden service", slug="hidden-service", description="Private", is_published=False, display_order=99)

    def test_services_page_displays_seven_official_services(self):
        response = self.client.get(reverse("services:list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["services"]), 7)
        self.assertContains(response, "Shared Infrastructure")
        self.assertContains(response, "Research and Development")

    def test_unpublished_service_is_hidden(self):
        self.assertNotContains(self.client.get(reverse("services:list")), "Hidden service")
