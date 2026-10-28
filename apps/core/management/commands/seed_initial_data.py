from django.core.management.base import BaseCommand

from apps.services.models import Service
from apps.core.models import ChairMessage, CoreValue, FocusArea, PageBanner, Program, SiteSettings


class Command(BaseCommand):
    help = "Seed verified institutional and clearly identified general content without duplicating records."

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
            "about": ("About Tsavo Innovation & Incubation Hub", "Creating an environment where innovation and entrepreneurship can flourish.", "Entrepreneurs collaborating during a mentoring session"),
            "services": ("Our Services", "Supporting innovators and entrepreneurs from ideas to sustainable ventures.", "Students taking part in a practical innovation workshop"),
            "projects": ("Innovation Projects", "Discovering ideas and innovations with the potential to create real-world impact.", "An agritech prototype being tested in the field"),
            "team": ("Meet Our Team", "The people supporting innovation, entrepreneurship and incubation at TIIH.", "A collaborative university innovation team"),
            "contact": ("Contact Us", "Connect with the Tsavo Innovation & Incubation Hub.", "A welcoming university innovation workspace"),
        }
        for page, (heading, text, alt) in banners.items():
            self._seed(PageBanner, {"page": page}, {"heading": heading, "supporting_text": text, "image_alt_text": alt}, reset)

        services = [
            ("Shared Infrastructure", "shared-infrastructure", "Access to appropriate shared facilities and infrastructure that support innovation, collaboration and entrepreneurship.", "bi-building-gear"),
            ("Business Advisory Services", "business-advisory-services", "Practical advisory support for business planning, venture development, market understanding and sustainable growth.", "bi-briefcase"),
            ("Financial Services", "financial-services", "Financial guidance and linkages to relevant funding opportunities. Funding, grants and loans are not guaranteed.", "bi-graph-up-arrow"),
            ("People Connectivity", "people-connectivity", "Mentorship, coaching, peer exchange, entrepreneurial networks and connections to relevant markets and value-chain participants.", "bi-people"),
            ("Customized Training", "customized-training", "Targeted technical, business-management and personal entrepreneurial skills development for innovators and venture teams.", "bi-mortarboard"),
            ("Ideation and Business Modeling", "ideation-and-business-modeling", "Structured support for problem discovery, idea development, business-model refinement and venture planning.", "bi-diagram-3"),
            ("Research and Development", "research-and-development", "Research-driven innovation, responsible prototyping and product-development support at an appropriate stage.", "bi-flask"),
        ]
        for order, (name, slug, description, icon) in enumerate(services, 1):
            self._seed(Service, {"slug": slug}, {"name": name, "description": description, "icon": icon, "display_order": order, "is_published": True}, reset)

        values = [
            ("Innovativeness", "We approach challenges with curiosity, creativity and a commitment to useful new ideas.", "bi-lightbulb"),
            ("Excellence", "We pursue high standards in learning, service, collaboration and the ventures we support.", "bi-award"),
            ("Entrepreneurship", "We nurture initiative, resilience and responsible value creation.", "bi-rocket-takeoff"),
            ("Professionalism", "We work with integrity, respect, accountability and care.", "bi-shield-check"),
        ]
        for order, (name, description, icon) in enumerate(values, 1):
            self._seed(CoreValue, {"name": name}, {"description": description, "icon": icon, "display_order": order}, reset)

        focus_areas = [
            ("Agriculture", "Ideas that strengthen productivity, resilience, value addition and market access.", "bi-flower1"),
            ("Mining", "Responsible technologies and enterprise models relevant to mineral resources and value chains.", "bi-gem"),
            ("Tourism", "Innovations that enrich visitor experiences and support sustainable local enterprise.", "bi-compass"),
            ("Blue Economy", "Solutions connected to sustainable water-based resources, livelihoods and ecosystems.", "bi-water"),
            ("Health", "Practical ideas that contribute to accessible, responsive and resilient health solutions.", "bi-heart-pulse"),
            ("Cross-cutting Areas", "Business development, ICT and education solutions that enable progress across sectors.", "bi-grid"),
        ]
        for order, (name, description, icon) in enumerate(focus_areas, 1):
            self._seed(FocusArea, {"name": name}, {"description": description, "icon": icon, "display_order": order}, reset)

        programs = [
            ("Innovation Incubation", "Structured support that helps innovators develop ideas into responsible and sustainable ventures.", "bi-boxes"),
            ("Mentorship and Coaching", "Guidance and reflective support for innovators navigating technical and entrepreneurial decisions.", "bi-people"),
            ("Entrepreneurial Skills Training", "Practical learning in venture planning, management and personal entrepreneurial capability.", "bi-mortarboard"),
            ("Ideation and Business Modeling", "Tools for understanding problems, testing assumptions and shaping viable business models.", "bi-bezier2"),
            ("Commercialization Support", "General guidance for preparing appropriate innovations for markets and value-chain connections.", "bi-shop-window"),
        ]
        for order, (title, description, icon) in enumerate(programs, 1):
            self._seed(Program, {"title": title}, {"description": description, "icon": icon, "display_order": order, "is_published": True}, reset)

        self._seed(ChairMessage, {"pk": 1}, {
            "chair_name": "Dr. Mwakio Mwagandi",
            "official_position": "Chair, Tsavo Innovation & Incubation Hub",
            "message": (
                "Welcome to the Tsavo Innovation & Incubation Hub, where ideas are nurtured into "
                "practical solutions and sustainable ventures. TIIH brings together students, "
                "researchers, entrepreneurs, industry partners and communities to learn, experiment "
                "and build with purpose. Through mentorship, skills development and collaborative "
                "networks, we help innovators move confidently from concept to impact. Whether you "
                "are shaping a new idea, strengthening an enterprise or seeking partnership, we invite "
                "you to engage with TIIH and help build an innovative, inclusive and enterprising future."
            ),
            "is_published": True,
        }, reset)
        self.stdout.write(self.style.SUCCESS("Initial TIIH content is ready."))

    @staticmethod
    def _seed(model, lookup, defaults, reset):
        if reset:
            model.objects.update_or_create(**lookup, defaults=defaults)
        else:
            model.objects.get_or_create(**lookup, defaults=defaults)

