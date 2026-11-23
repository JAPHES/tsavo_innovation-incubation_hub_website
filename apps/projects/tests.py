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
        listing = self.client.get(reverse("projects:list"))
        self.assertEqual(listing.status_code, 200)
        self.assertNotContains(listing, "projects found")
        self.assertEqual(listing.context["page_obj"][0].slug, "upcycled-cotton-hydro-pellets")
        project = InnovationProject.objects.get(slug="upcycled-cotton-hydro-pellets")
        response = self.client.get(project.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, project.title)
        self.assertContains(response, '<img class="project-hero-image"')
        self.assertNotContains(response, "style=")

    def test_search_and_filters(self):
        response = self.client.get(reverse("projects:list"), {"q": "project 2"})
        self.assertContains(response, "Published project 2")
        response = self.client.get(reverse("projects:list"), {"category": "ict", "stage": "research"})
        self.assertTrue(all(item.category == "ict" and item.development_stage == "research" for item in response.context["page_obj"]))

    def test_long_anonymous_search_terms_are_bounded(self):
        response = self.client.get(reverse("projects:list"), {"q": "x" * 1000})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["query"]), 120)

    def test_pagination_and_filter_preservation(self):
        response = self.client.get(reverse("projects:list"), {"page": 2, "category": "agriculture"})
        self.assertEqual(response.status_code, 200)
        filtered = self.client.get(reverse("projects:list"), {"q": "Published"})
        self.assertContains(filtered, "q=Published")

    def test_unpublished_project_is_not_public(self):
        InnovationProject.objects.filter(slug="private-draft").update(details_public=True)
        response = self.client.get(reverse("projects:detail", kwargs={"slug": "private-draft"}))
        self.assertEqual(response.status_code, 404)

    def test_only_hydro_pellets_has_a_public_detail_link(self):
        project = InnovationProject.objects.get(slug="upcycled-cotton-hydro-pellets")
        closed_project = InnovationProject.objects.get(slug="blood-bank-management-system")
        self.assertEqual(self.client.get(project.get_absolute_url()).status_code, 200)
        self.assertEqual(self.client.get(closed_project.get_absolute_url()).status_code, 404)
        listing = self.client.get(reverse("projects:list"))
        self.assertContains(listing, "View project", count=1)
        self.assertContains(listing, f'href="{project.get_absolute_url()}"')
        self.assertNotContains(listing, f'href="{closed_project.get_absolute_url()}"')
        homepage = self.client.get(reverse("core:home"))
        self.assertContains(homepage, "View project", count=1)
        self.assertContains(homepage, f'href="{project.get_absolute_url()}"')
        self.assertNotContains(homepage, f'href="{closed_project.get_absolute_url()}"')
        sitemap = self.client.get("/sitemap.xml")
        self.assertContains(sitemap, project.get_absolute_url())
        self.assertNotContains(sitemap, closed_project.get_absolute_url())

    def test_another_project_can_be_opened_individually_later(self):
        project = InnovationProject.objects.get(slug="blood-bank-management-system")
        project.details_public = True
        project.save(update_fields=["details_public"])
        self.assertContains(self.client.get(reverse("projects:list")), "View project", count=2)
        self.assertEqual(self.client.get(project.get_absolute_url()).status_code, 200)


class PresentationProjectTests(TestCase):
    def test_only_hydro_pellets_presentation_detail_is_public(self):
        for slug, title in (
            ("upcycled-cotton-hydro-pellets", "Upcycled Cotton Hydro-Pellets"),
            ("ai-multilingual-learning-platform", "AI-Powered Multilingual Learning Platform"),
            ("blue-bin", "Blue Bin"),
        ):
            with self.subTest(slug=slug):
                project = InnovationProject.objects.get(slug=slug)
                self.assertTrue(project.is_published)
                self.assertEqual(project.is_featured, slug != "ai-multilingual-learning-platform")
                self.assertEqual(project.development_stage, "")
                self.assertEqual(project.details_public, slug == "upcycled-cotton-hydro-pellets")
                response = self.client.get(project.get_absolute_url())
                if project.details_public:
                    self.assertContains(response, title)
                else:
                    self.assertEqual(response.status_code, 404)

    def test_blood_bank_is_featured_and_education_remains_in_catalogue(self):
        blood_bank = InnovationProject.objects.get(slug="blood-bank-management-system")
        self.assertTrue(blood_bank.is_published)
        self.assertTrue(blood_bank.is_featured)
        self.assertEqual(blood_bank.homepage_order, 20)
        self.assertEqual(blood_bank.category, "health")
        self.assertEqual(blood_bank.development_stage, "")
        self.assertFalse(blood_bank.details_public)
        self.assertEqual(self.client.get(blood_bank.get_absolute_url()).status_code, 404)
        self.assertContains(self.client.get(reverse("projects:list")), "AI-Powered Multilingual Learning Platform")

    def test_blue_bin_shows_only_confirmed_information(self):
        project = InnovationProject.objects.get(slug="blue-bin")
        self.assertEqual(project.category, "")
        self.assertEqual(project.problem_statement, "")
        self.assertEqual(project.proposed_solution, "")
        self.assertEqual(self.client.get(project.get_absolute_url()).status_code, 404)
        project.details_public = True
        project.save(update_fields=["details_public"])
        response = self.client.get(project.get_absolute_url())
        self.assertContains(response, "Pwani Innovation Week 2025")
        self.assertContains(response, "Pwani Innovation Week 2025 online pitch competition")
        self.assertContains(response, "images/innovations/blue-bin-pwani-innovation-week.png")
        self.assertNotContains(response, "images/innovations/blue-bin-pwani-group.jpeg")
        self.assertNotContains(response, "Further information")
        self.assertNotContains(response, "Development stage")
