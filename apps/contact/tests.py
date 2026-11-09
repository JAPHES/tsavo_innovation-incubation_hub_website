from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage


class ContactPageTests(TestCase):
    def setUp(self):
        self.url = reverse("contact:contact")

    def test_contact_page_shows_direct_details_and_campus_map(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tiih@ttu.ac.ke")
        self.assertContains(response, "+254 722 274257")
        self.assertContains(response, "Taita Taveta University")
        self.assertContains(response, "Runda, Room C14")
        self.assertContains(response, "Health Unit")
        self.assertContains(response, "google.com/maps?q=Taita+Taveta+University")
        self.assertNotContains(response, "Send an inquiry")
        self.assertNotContains(response, '<form class="contact-form"')

    def test_contact_submissions_are_disabled(self):
        response = self.client.post(self.url, {"message": "This form is closed"})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_historical_messages_are_not_rendered_publicly(self):
        ContactMessage.objects.create(
            full_name="Private", email="private@example.com", subject="Confidential phrase",
            message="Secret body", consent=True,
        )
        response = self.client.get(self.url)
        self.assertNotContains(response, "Confidential phrase")
