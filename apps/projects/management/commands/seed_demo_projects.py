from django.core.management.base import BaseCommand

from apps.projects.models import InnovationProject


class Command(BaseCommand):
    help = "Create clearly labelled, unpublished demonstration projects for local testing."

    def handle(self, *args, **options):
        demos = [
            ("[DEMO] Climate-smart irrigation concept", "demo-climate-smart-irrigation", "agriculture", "prototype"),
            ("[DEMO] Community tourism planning tool", "demo-community-tourism-tool", "tourism", "idea"),
            ("[DEMO] Mineral traceability study", "demo-mineral-traceability", "mining", "research"),
        ]
        for title, slug, category, stage in demos:
            InnovationProject.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "short_description": "Demonstration content for testing the website layout. This is not an official TIIH project.",
                    "full_description": "This unpublished record exists only to help administrators preview project content fields.",
                    "category": category,
                    "development_stage": stage,
                    "is_featured": False,
                    "is_published": False,
                },
            )
        self.stdout.write(self.style.SUCCESS("Unpublished demonstration projects are ready."))
