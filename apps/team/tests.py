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

    def test_chair_is_first_and_uses_supplied_portrait(self):
        response = self.client.get(reverse("team:list"))
        html = response.content.decode()
        self.assertLess(html.index("Dr. Mwakio Mwagandi"), html.index("First Active"))
        self.assertContains(response, "Chair, Tsavo Innovation &amp; Incubation Hub")
        self.assertContains(response, "images/team/chair_dr_mwakio_mwagandi.jpg")

    def test_chair_linkedin_profile_appears_when_set(self):
        chair = TeamMember.objects.get(full_name="Dr. Mwakio Mwagandi")
        self.assertNotContains(self.client.get(reverse("team:list")), "LinkedIn profile")
        chair.linkedin_url = "https://www.linkedin.com/in/example-chair/"
        chair.save(update_fields=["linkedin_url"])
        response = self.client.get(reverse("team:list"))
        self.assertContains(response, 'href="https://www.linkedin.com/in/example-chair/"')
        self.assertContains(response, "LinkedIn profile")
