from types import SimpleNamespace

from .models import PageBanner

BANNER_FALLBACKS = {
    "home": "images/banners/tiih_training_hero.png",
    "about": "images/banners/tiih_outreach_about.jpeg",
    "services": "images/banners/tiih_training_hero.png",
    "projects": "images/banners/tiih_training_hero.png",
    "team": "images/banners/tiih_training_hero.png",
    "contact": "images/banners/tiih_training_hero.png",
    "programmes": "images/banners/tiih_training_hero.png",
    "partners": "images/banners/tiih_outreach_about.jpeg",
}
BANNER_FALLBACK_ALTS = {
    "home": "Participants working with laptops during a TIIH training session",
    "about": "A speaker addressing students during a TIIH outreach session",
    "services": "Participants working with laptops during a TIIH training session",
    "projects": "Participants working with laptops during a TIIH training session",
    "team": "Participants working with laptops during a TIIH training session",
    "contact": "Participants working with laptops during a TIIH training session",
    "programmes": "Participants working with laptops during a TIIH training session",
    "partners": "A speaker addressing students during a TIIH outreach session",
}
BANNER_DEFAULTS = {
    "home": ("Cultivating Entrepreneurs", "Empowering innovators, nurturing entrepreneurship, and transforming ideas into sustainable ventures."),
    "about": ("Where Innovation Takes Root", "Discover the purpose, vision and values guiding a hub built to turn ideas into meaningful enterprise and impact."),
    "services": ("Our Services", "Supporting innovators and entrepreneurs from ideas to sustainable ventures."),
    "projects": ("Featured Innovations", "Discovering ideas and innovations with the potential to create real-world impact."),
    "team": ("Meet Our Team", "The people supporting innovation, entrepreneurship and incubation at TIIH."),
    "contact": ("Contact Us", "Connect with the Tsavo Innovation & Incubation Hub."),
    "programmes": ("Programmes and Events", "Learning, collaboration and practical experience for emerging entrepreneurs."),
    "partners": ("Collaborations & Partnerships", "Working with institutions and networks to support innovation and enterprise."),
}

CHAIR_MESSAGE = SimpleNamespace(
    chair_name="Dr. Mwakio Mwagandi",
    official_position="Chairman, Tsavo Innovation & Incubation Hub",
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
    SimpleNamespace(name="Research and Development", slug="research-and-development", description="Research-driven innovation, responsible prototyping and product-development support at an appropriate stage.", icon="bi-clipboard-data"),
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

PROGRAMME_HIGHLIGHTS = (
    SimpleNamespace(
        title="Huduma Whitebox Entrepreneurship Boot Camp",
        label="Entrepreneurship training",
        description=(
            "On 29 September 2026, Taita Taveta University and TIIH collaborated with the "
            "ICT Authority to deliver a one-day entrepreneurship boot camp for TTU students. "
            "The sessions covered entrepreneurship, business modelling, product development "
            "and market-entry strategy, helping innovators explore how to turn ideas into "
            "commercially viable products."
        ),
        date="29 September 2026",
        venue="Taita Taveta University",
    ),
    SimpleNamespace(
        title="Youth Entrepreneurship and Innovation Readiness Pilot",
        label="Africa 2100 partnership",
        description=(
            "TIIH has partnered with Africa 2100 NFP, a Chicago-registered public charity, "
            "to implement a pilot that helps underserved young people build entrepreneurship "
            "readiness through mobile-first education, mentorship and pathways to opportunity."
        ),
        logo="images/partners/africa-2100-logo.png",
        logo_alt="Africa 2100 logo",
    ),
    SimpleNamespace(
        title="African Social Venture Incubation",
        label="Online entrepreneurship course",
        description=(
            "Working with the Cambridge Centre for Social Innovation and Mbeya University "
            "of Science and Technology, TIIH offered an online course for entrepreneurs in "
            "Kenya and Tanzania developing purpose-driven ventures that respond to societal "
            "challenges. The course was funded by the Mastercard Foundation."
        ),
        logo="images/partners/cambridge-judge-logo.png",
        logo_alt="University of Cambridge Judge Business School logo",
    ),
)

PARTNERS = (
    SimpleNamespace(
        name="Mbeya University of Science and Technology",
        location="Tanzania",
        logo="images/partners/mbeya-university-logo.jpg",
        logo_alt="Mbeya University of Science and Technology emblem",
        url="https://must.ac.tz/",
    ),
    SimpleNamespace(
        name="Cambridge Centre for Social Innovation",
        location="Cambridge Judge Business School, UK",
        logo="images/partners/cambridge-judge-logo.png",
        logo_alt="Cambridge Judge Business School logo",
        url="https://www.jbs.cam.ac.uk/centres/social-innovation/",
    ),
    SimpleNamespace(
        name="Africa 2100 NFP",
        location="United States",
        logo="images/partners/africa-2100-logo.png",
        logo_alt="Africa 2100 logo",
        url="https://www.africa2100.org/",
    ),
    SimpleNamespace(
        name="Coast Innovation Hubs Network",
        location="Kenya",
        logo="",
        logo_alt="",
        url="",
    ),
    SimpleNamespace(
        name="Government of Taita Taveta County",
        location="Kenya",
        logo="images/partners/taita-taveta-county-logo.png",
        logo_alt="Taita Taveta County Government emblem",
        url="https://www.taitataveta.go.ke/",
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
        "banner_fallback_alt": BANNER_FALLBACK_ALTS[page],
        "banner_page": page,
    }
