from django.test import TestCase
from django.urls import reverse

from .models import TeamMember


class TeamPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        TeamMember.objects.create(full_name="Second Active", role="Mentor", biography="Approved bio", display_order=2)
        TeamMember.objects.create(full_name="First Active", role="Coordinator", biography="Approved bio", display_order=1)
        TeamMember.objects.create(full_name="Inactive Person", role="Private", biography="Not public", is_active=False)

    def test_active_profiles_only_and_display_order(self):
        response = self.client.get(reverse("team:list"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Inactive Person")
        html = response.content.decode()
        self.assertLess(html.index("First Active"), html.index("Second Active"))
