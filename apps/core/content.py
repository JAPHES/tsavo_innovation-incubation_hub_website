from types import SimpleNamespace

from .models import PageBanner

BANNER_FALLBACKS = {
    "home": "images/banners/home_hero.jpg", "about": "images/banners/about_banner.jpg",
    "services": "images/banners/services_banner.jpg", "projects": "images/banners/projects_banner.jpg",
    "team": "images/banners/team_banner.jpg", "contact": "images/banners/contact_banner.jpg",
}
BANNER_DEFAULTS = {
    "home": ("Cultivating Entrepreneurs", "Empowering innovators, nurturing entrepreneurship, and transforming ideas into sustainable ventures."),
    "about": ("About Tsavo Innovation & Incubation Hub", "Creating an environment where innovation and entrepreneurship can flourish."),
    "services": ("Our Services", "Supporting innovators and entrepreneurs from ideas to sustainable ventures."),
    "projects": ("Innovation Projects", "Discovering ideas and innovations with the potential to create real-world impact."),
    "team": ("Meet Our Team", "The people supporting innovation, entrepreneurship and incubation at TIIH."),
    "contact": ("Contact Us", "Connect with the Tsavo Innovation & Incubation Hub."),
}

SAMPLE_INNOVATIONS = (
    SimpleNamespace(
        preview_only=True,
        title="SolarSmart Irrigation Kit",
        short_description="A solar-powered soil-moisture monitoring concept designed to help smallholder farmers use water more efficiently.",
        category_label="Agriculture",
        stage_label="Prototype concept",
        icon="bi-droplet-half",
    ),
    SimpleNamespace(
        preview_only=True,
        title="EcoBrick Circular Build Lab",
        short_description="A circular-economy concept exploring how recovered plastic can become durable modular materials for local construction.",
        category_label="Sustainable materials",
        stage_label="Testing concept",
        icon="bi-recycle",
    ),
    SimpleNamespace(
        preview_only=True,
        title="Jirani Market Link",
        short_description="A mobile marketplace concept connecting local producers with buyers, logistics support and practical market information.",
        category_label="ICT & enterprise",
        stage_label="Incubation concept",
        icon="bi-phone",
    ),
)


def banner_context(page):
    banner = PageBanner.objects.filter(page=page).first()
    if banner is None:
        heading, supporting_text = BANNER_DEFAULTS[page]
        banner = SimpleNamespace(
            heading=heading,
            supporting_text=supporting_text,
            image_alt_text=f"{heading} banner",
            background_image=None,
        )
    return {
        "banner": banner,
        "banner_fallback": BANNER_FALLBACKS[page],
        "banner_page": page,
    }
