from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import ContactMessage


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class ContactFormTests(TestCase):
    def setUp(self):
        cache.clear()
        self.url = reverse("contact:contact")
        self.valid_data = {
            "full_name": "Site Visitor", "email": "visitor@example.com", "phone": "+254700000000",
            "subject": "Innovation inquiry", "message": "I would like to discuss an innovation idea.",
            "consent": "on", "website": "",
        }

    def test_required_fields_and_invalid_email(self):
        self.assertContains(self.client.post(self.url, {}), "This field is required")
        invalid = dict(self.valid_data, email="not-an-email")
        self.assertContains(self.client.post(self.url, invalid), "Enter a valid email address")

    def test_valid_submission_is_saved_and_redirected_with_feedback(self):
        response = self.client.post(self.url, self.valid_data, follow=True)
        self.assertRedirects(response, self.url)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertContains(response, "Your message has been received")

    def test_duplicate_post_in_same_session_is_not_saved_twice(self):
        self.client.post(self.url, self.valid_data)
        self.client.post(self.url, self.valid_data)
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_csrf_is_enforced(self):
        csrf_client = Client(enforce_csrf_checks=True)
        self.assertEqual(csrf_client.post(self.url, self.valid_data).status_code, 403)

    def test_saved_message_is_not_rendered_publicly(self):
        ContactMessage.objects.create(full_name="Private", email="private@example.com", subject="Confidential phrase", message="Secret body", consent=True)
        response = self.client.get(self.url)
        self.assertNotContains(response, "Confidential phrase")
