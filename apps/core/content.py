from types import SimpleNamespace

from .models import PageBanner

BANNER_FALLBACKS = {
    "home": "images/banners/home_hero.jpg", "about": "images/banners/about_banner.jpg",
    "services": "images/banners/services_banner.jpg", "projects": "images/banners/projects_banner.jpg",
    "team": "images/banners/team_banner.jpg", "contact": "images/banners/contact_banner.jpg",
}
BANNER_DEFAULTS = {
    "home": ("Cultivating Entrepreneurs", "Empowering innovators, nurturing entrepreneurship, and transforming ideas into sustainable ventures."),
    "about": ("Where Innovation Takes Root", "Discover the purpose, vision and values guiding a hub built to turn ideas into meaningful enterprise and impact."),
    "services": ("Our Services", "Supporting innovators and entrepreneurs from ideas to sustainable ventures."),
    "projects": ("Innovation Projects", "Discovering ideas and innovations with the potential to create real-world impact."),
    "team": ("Meet Our Team", "The people supporting innovation, entrepreneurship and incubation at TIIH."),
    "contact": ("Contact Us", "Connect with the Tsavo Innovation & Incubation Hub."),
}

CHAIR_MESSAGE = SimpleNamespace(
    chair_name="Dr. Mwakio Mwagandi",
    official_position="Chair, Tsavo Innovation & Incubation Hub",
    photograph=None,
    message=(
        "Welcome to the Tsavo Innovation & Incubation Hub, where ideas are nurtured into "
        "practical solutions and sustainable ventures. TIIH brings together students, "
        "researchers, entrepreneurs, industry partners and communities to learn, experiment "
        "and build with purpose. Through mentorship, skills development and collaborative "
        "networks, we help innovators move confidently from concept to impact. Whether you "
        "are shaping a new idea, strengthening an enterprise or seeking partnership, we invite "
        "you to engage with TIIH and help build an innovative, inclusive and enterprising future."
    ),
)

SERVICES = (
    SimpleNamespace(name="Shared Infrastructure", slug="shared-infrastructure", description="Access to appropriate shared facilities and infrastructure that support innovation, collaboration and entrepreneurship.", icon="bi-building-gear"),
    SimpleNamespace(name="Business Advisory Services", slug="business-advisory-services", description="Practical advisory support for business planning, venture development, market understanding and sustainable growth.", icon="bi-briefcase"),
    SimpleNamespace(name="Financial Services", slug="financial-services", description="Financial guidance and linkages to relevant funding opportunities. Funding, grants and loans are not guaranteed.", icon="bi-graph-up-arrow"),
    SimpleNamespace(name="People Connectivity", slug="people-connectivity", description="Mentorship, coaching, peer exchange, entrepreneurial networks and connections to relevant markets and value-chain participants.", icon="bi-people"),
    SimpleNamespace(name="Customized Training", slug="customized-training", description="Targeted technical, business-management and personal entrepreneurial skills development for innovators and venture teams.", icon="bi-mortarboard"),
    SimpleNamespace(name="Ideation and Business Modeling", slug="ideation-and-business-modeling", description="Structured support for problem discovery, idea development, business-model refinement and venture planning.", icon="bi-diagram-3"),
    SimpleNamespace(name="Research and Development", slug="research-and-development", description="Research-driven innovation, responsible prototyping and product-development support at an appropriate stage.", icon="bi-flask"),
)

CORE_VALUES = (
    SimpleNamespace(name="Innovativeness", description="We approach challenges with curiosity, creativity and a commitment to useful new ideas.", icon="bi-lightbulb"),
    SimpleNamespace(name="Excellence", description="We pursue high standards in learning, service, collaboration and the ventures we support.", icon="bi-award"),
    SimpleNamespace(name="Entrepreneurship", description="We nurture initiative, resilience and responsible value creation.", icon="bi-rocket-takeoff"),
    SimpleNamespace(name="Professionalism", description="We work with integrity, respect, accountability and care.", icon="bi-shield-check"),
)

FOCUS_AREAS = (
    SimpleNamespace(name="Agriculture", description="Ideas that strengthen productivity, resilience, value addition and market access.", icon="bi-flower1"),
    SimpleNamespace(name="Mining", description="Responsible technologies and enterprise models relevant to mineral resources and value chains.", icon="bi-gem"),
    SimpleNamespace(name="Tourism", description="Innovations that enrich visitor experiences and support sustainable local enterprise.", icon="bi-compass"),
    SimpleNamespace(name="Blue Economy", description="Solutions connected to sustainable water-based resources, livelihoods and ecosystems.", icon="bi-water"),
    SimpleNamespace(name="Health", description="Practical ideas that contribute to accessible, responsive and resilient health solutions.", icon="bi-heart-pulse"),
    SimpleNamespace(name="Cross-cutting Areas", description="Business development, ICT and education solutions that enable progress across sectors.", icon="bi-grid"),
)

PROGRAMS = (
    SimpleNamespace(title="Innovation Incubation", description="Structured support that helps innovators develop ideas into responsible and sustainable ventures.", icon="bi-boxes", application_url=""),
    SimpleNamespace(title="Mentorship and Coaching", description="Guidance and reflective support for innovators navigating technical and entrepreneurial decisions.", icon="bi-people", application_url=""),
    SimpleNamespace(title="Entrepreneurial Skills Training", description="Practical learning in venture planning, management and personal entrepreneurial capability.", icon="bi-mortarboard", application_url=""),
    SimpleNamespace(title="Ideation and Business Modeling", description="Tools for understanding problems, testing assumptions and shaping viable business models.", icon="bi-bezier2", application_url=""),
    SimpleNamespace(title="Commercialization Support", description="General guidance for preparing appropriate innovations for markets and value-chain connections.", icon="bi-shop-window", application_url=""),
)

SAMPLE_INNOVATIONS = (
    SimpleNamespace(
        preview_only=True,
        title="SolarSmart Irrigation Kit",
        short_description="A solar-powered soil-moisture monitoring system designed to help smallholder farmers use water more efficiently.",
        category_label="Agriculture",
        stage_label="Prototype",
        image="images/innovations/solarsmart-irrigation.jpg",
        image_alt="A university innovation team testing a solar-powered smart irrigation system",
    ),
    SimpleNamespace(
        preview_only=True,
        title="EcoBrick Circular Build Lab",
        short_description="A circular-economy initiative transforming recovered plastic into durable modular materials for local construction.",
        category_label="Sustainable materials",
        stage_label="Pilot testing",
        image="images/innovations/ecobrick-build-lab.jpg",
        image_alt="A university innovation team producing construction bricks from recovered plastic",
    ),
    SimpleNamespace(
        preview_only=True,
        title="Jirani Market Link",
        short_description="A mobile marketplace platform connecting local producers with buyers, logistics support and practical market information.",
        category_label="ICT & enterprise",
        stage_label="Incubation",
        image="images/innovations/jirani-market-link.jpg",
        image_alt="A digital innovation team demonstrating a mobile market platform to a produce entrepreneur",
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
