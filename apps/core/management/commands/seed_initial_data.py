from django.core.management.base import BaseCommand

from apps.core.models import PageBanner, SiteSettings


class Command(BaseCommand):
    help = "Seed database-backed site settings and page banners without duplicating records."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Restore seeded records to their supplied defaults.")

    def handle(self, *args, **options):
        reset = options["reset"]

        site_defaults = {
            "website_name": "Tsavo Innovation & Incubation Hub",
            "abbreviation": "TIIH",
            "tagline": "Cultivating Entrepreneurs",
            "contact_email": "tiih@ttu.ac.ke",
            "contact_phone": "+254 722 274257",
            "description": "TIIH operates under Taita Taveta University and supports innovation, business incubation, entrepreneurship, mentoring, training and the commercialization of innovations.",
            "vision": "A flourishing society powered by innovation and entrepreneurship",
            "mission": "To create an environment that nurtures the spawning of a dynamic community of entrepreneurs who produce sustainable ventures that positively impact livelihoods",
            "main_objective": "To create entrepreneurs through innovation, business incubation, and development.",
        }
        self._seed(SiteSettings, {"pk": 1}, site_defaults, reset)

        banners = {
            "home": ("Cultivating Entrepreneurs", "Empowering innovators, nurturing entrepreneurship, and transforming ideas into sustainable ventures.", "Students collaborating in a university innovation workspace"),
            "about": ("Where Innovation Takes Root", "Discover the purpose, vision and values guiding a hub built to turn ideas into meaningful enterprise and impact.", "Entrepreneurs collaborating during a mentoring session"),
            "services": ("Our Services", "Supporting innovators and entrepreneurs from ideas to sustainable ventures.", "Students taking part in a practical innovation workshop"),
            "projects": ("Innovation Projects", "Discovering ideas and innovations with the potential to create real-world impact.", "An agritech prototype being tested in the field"),
            "team": ("Meet Our Team", "The people supporting innovation, entrepreneurship and incubation at TIIH.", "A collaborative university innovation team"),
            "contact": ("Contact Us", "Connect with the Tsavo Innovation & Incubation Hub.", "A welcoming university innovation workspace"),
        }
        for page, (heading, text, alt) in banners.items():
            self._seed(PageBanner, {"page": page}, {"heading": heading, "supporting_text": text, "image_alt_text": alt}, reset)
        self.stdout.write(self.style.SUCCESS("Database-backed TIIH settings and banners are ready."))

    @staticmethod
    def _seed(model, lookup, defaults, reset):
        if reset:
            model.objects.update_or_create(**lookup, defaults=defaults)
        else:
            model.objects.get_or_create(**lookup, defaults=defaults)

