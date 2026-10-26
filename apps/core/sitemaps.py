from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.projects.models import InnovationProject


class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return ["core:home", "core:about", "services:list", "projects:list", "team:list", "contact:contact"]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return InnovationProject.objects.filter(is_published=True)

    def lastmod(self, item):
        return item.updated_at
