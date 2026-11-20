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
        self.assertEqual(len(response.context["members"]), TeamMember.objects.filter(is_active=True).count())
        self.assertEqual(response.context["members"][0].full_name, "Dr. Mwakio Mwagandi")
        html = response.content.decode()
        self.assertEqual(html.count('<article class="team-card'), len(response.context["members"]))
        self.assertEqual(html.count('class="team-linkedin"'), len(response.context["members"]))
        self.assertLess(html.index("First Active"), html.index("Second Active"))

    def test_chair_is_first_and_uses_supplied_portrait(self):
        response = self.client.get(reverse("team:list"))
        html = response.content.decode()
        self.assertLess(html.index("Dr. Mwakio Mwagandi"), html.index("First Active"))
        self.assertContains(response, "Chairman, Tsavo Innovation &amp; Incubation Hub")
        self.assertContains(response, "images/team/chair_dr_mwakio_mwagandi.jpg")

    def test_feedback_members_appear_without_invented_profiles(self):
        response = self.client.get(reverse("team:list"))
        for name in (
            "Mrs Amina Ndinya", "Mr. Edwin Kirui", "Prof. Bernard Alunda",
            "Ms Belinda Owala", "Dr Rehema Swalehe", "Ms Leah Andisi",
            "Mr. Thomas Makungu", "Ms Anne Nyabuti",
        ):
            with self.subTest(name=name):
                member = TeamMember.objects.get(full_name=name)
                self.assertEqual(member.role, "")
                self.assertEqual(member.biography, "")
                self.assertContains(response, name)
                if name not in {"Mrs Amina Ndinya", "Ms Anne Nyabuti"}:
                    self.assertContains(response, f"Portrait not yet available for {name}")

    def test_supplied_member_portraits_are_used(self):
        response = self.client.get(reverse("team:list"))
        self.assertContains(response, "images/team/amina_ndinya.jpeg")
        self.assertContains(response, "images/team/anne_nyabuti.jpeg")
        self.assertNotContains(response, "Portrait not yet available for Mrs Amina Ndinya")
        self.assertNotContains(response, "Portrait not yet available for Ms Anne Nyabuti")

    def test_chair_profile_and_fallback_linkedin_contact(self):
        chair = TeamMember.objects.get(full_name="Dr. Mwakio Mwagandi")
        response = self.client.get(reverse("team:list"))
        self.assertEqual(chair.linkedin_url, "https://www.linkedin.com/in/dr-mwakio-wa-mwagandi-phd-34b20119/")
        self.assertContains(response, f'href="{chair.linkedin_url}"')
        self.assertNotContains(response, "Temporary LinkedIn contact")
        self.assertContains(response, "Open Japhes Murithi's LinkedIn profile")
        self.assertContains(response, 'href="https://www.linkedin.com/in/japhes-murithi-79178a329/"')

        amina = TeamMember.objects.get(full_name="Mrs Amina Ndinya")
        amina.linkedin_url = "https://www.linkedin.com/in/example-amina/"
        amina.save(update_fields=["linkedin_url"])
        response = self.client.get(reverse("team:list"))
        self.assertContains(response, 'href="https://www.linkedin.com/in/example-amina/"')
        self.assertContains(response, "View Mrs Amina Ndinya's LinkedIn profile")
