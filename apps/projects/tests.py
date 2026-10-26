from django.test import TestCase
from django.urls import reverse

from .models import InnovationProject


class ProjectPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for number in range(11):
            InnovationProject.objects.create(
                title=f"Published project {number}", slug=f"published-project-{number}",
                short_description="Approved public project", full_description="Project overview",
                category="agriculture" if number % 2 == 0 else "ict",
                development_stage="prototype" if number % 2 == 0 else "research",
                is_published=True,
            )
        InnovationProject.objects.create(
            title="Private draft", slug="private-draft", short_description="Not public",
            full_description="Draft", category="mining", development_stage="idea", is_published=False,
        )

    def test_listing_and_detail_routes_work(self):
        self.assertEqual(self.client.get(reverse("projects:list")).status_code, 200)
        project = InnovationProject.objects.filter(is_published=True).first()
        response = self.client.get(project.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, project.title)

    def test_search_and_filters(self):
        response = self.client.get(reverse("projects:list"), {"q": "project 2"})
        self.assertContains(response, "Published project 2")
        response = self.client.get(reverse("projects:list"), {"category": "ict", "stage": "research"})
        self.assertTrue(all(item.category == "ict" and item.development_stage == "research" for item in response.context["page_obj"]))

    def test_pagination_and_filter_preservation(self):
        response = self.client.get(reverse("projects:list"), {"page": 2, "category": "agriculture"})
        self.assertEqual(response.status_code, 200)
        filtered = self.client.get(reverse("projects:list"), {"q": "Published"})
        self.assertContains(filtered, "q=Published")

    def test_unpublished_project_is_not_public(self):
        response = self.client.get(reverse("projects:detail", kwargs={"slug": "private-draft"}))
        self.assertEqual(response.status_code, 404)
