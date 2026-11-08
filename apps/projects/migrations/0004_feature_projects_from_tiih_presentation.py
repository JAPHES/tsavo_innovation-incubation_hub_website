"""Publish projects described in the TIIH presentation supplied in November 2026.

The deck gives no development stage for these projects. Blue Bin's focus area and
technical description are also absent, so those fields remain empty.
"""

from django.db import migrations


PRESENTATION_PROJECTS = (
    {
        "slug": "blue-bin",
        "title": "Blue Bin",
        "short_description": (
            "Blue Bin from Taita Taveta University was listed as a runner-up in the "
            "Pwani Innovation Week 2025 online pitch competition."
        ),
        "full_description": (
            "Blue Bin, a Taita Taveta University entry, was listed as a runner-up "
            "in the Pwani Innovation Week 2025 online pitch competition."
        ),
        "category": "",
        "development_stage": "",
    },
    {
        "slug": "ai-multilingual-learning-platform",
        "title": "AI-Powered Multilingual Learning Platform",
        "short_description": (
            "A platform in development to make learning content more accessible and "
            "culturally relevant for marginalized communities in Eastern Africa."
        ),
        "full_description": (
            "The TIIH presentation describes an AI-powered multilingual learning "
            "platform being developed for marginalized ethnic communities in "
            "Eastern Africa. Its aim is to make educational content more accessible, "
            "relevant and culturally sensitive. The proposed methods are designed "
            "to be adaptable to other marginalized communities.\n\n"
            "The presentation reports that a Taita Taveta University student "
            "received a grant through the 2024–2025 Youth and Multilingualism "
            "AI Incubator programme."
        ),
        "problem_statement": (
            "Marginalized communities may lack educational content in languages "
            "and cultural contexts that serve their needs."
        ),
        "proposed_solution": (
            "Develop a multilingual learning platform using AI to support "
            "accessible, culturally relevant educational content."
        ),
        "key_features": (
            "AI-powered multilingual learning\n"
            "Culturally relevant educational content\n"
            "Approach designed for adaptation to other communities"
        ),
        "category": "education",
        "development_stage": "",
    },
    {
        "slug": "upcycled-cotton-hydro-pellets",
        "title": "Upcycled Cotton Hydro-Pellets",
        "short_description": (
            "Biodegradable soil-enhancing pellets made from second-hand clothing "
            "to support soil health and nutrient efficiency."
        ),
        "full_description": (
            "Upcycled Cotton Hydro-Pellets turns second-hand clothing (mitumba) "
            "into biodegradable pellets intended to improve soil health and "
            "nutrient efficiency while addressing textile pollution. The project "
            "is designed to support climate-resilient agriculture, especially "
            "in water-stressed regions.\n\n"
            "The TIIH presentation identifies it as a winner of the UNIDO Global "
            "Call University Track and describes an online incubation opportunity "
            "with UNIDO ITPO Bahrain."
        ),
        "problem_statement": (
            "Textile waste and the need for more resilient soil management "
            "present linked challenges in water-stressed agricultural regions."
        ),
        "proposed_solution": (
            "Develop biodegradable soil-enhancing pellets from second-hand "
            "clothing to support soil health and nutrient efficiency."
        ),
        "key_features": (
            "Uses upcycled second-hand clothing\n"
            "Designed to support soil health and nutrient efficiency\n"
            "Intended for climate-resilient agriculture"
        ),
        "category": "agriculture",
        "development_stage": "",
    },
)


def add_presentation_projects(apps, schema_editor):
    project_model = apps.get_model("projects", "InnovationProject")
    projects = project_model.objects.using(schema_editor.connection.alias)
    for project in PRESENTATION_PROJECTS:
        slug = project["slug"]
        defaults = {key: value for key, value in project.items() if key != "slug"}
        defaults.update(is_published=True, is_featured=True)
        projects.get_or_create(slug=slug, defaults=defaults)


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0003_alter_innovationproject_category_and_more"),
    ]

    operations = [
        migrations.RunPython(add_presentation_projects, migrations.RunPython.noop),
    ]
