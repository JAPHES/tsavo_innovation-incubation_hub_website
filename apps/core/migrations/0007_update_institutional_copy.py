from django.db import migrations


OLD_DESCRIPTION = (
    "TIIH operates under Taita Taveta University and supports innovation, business "
    "incubation, entrepreneurship, mentoring, training and the commercialization of innovations."
)
NEW_DESCRIPTION = (
    "TIIH is the organ of Taita Taveta University that supports innovation, business "
    "incubation, entrepreneurship, mentoring, training and the commercialization of innovations."
)


def update_default_copy(apps, schema_editor):
    database = schema_editor.connection.alias
    settings = apps.get_model("core", "SiteSettings")
    banners = apps.get_model("core", "PageBanner")
    settings.objects.using(database).filter(description=OLD_DESCRIPTION).update(description=NEW_DESCRIPTION)
    banners.objects.using(database).filter(page="projects", heading="Innovation Projects").update(
        heading="Featured Innovations"
    )


class Migration(migrations.Migration):
    dependencies = [("core", "0006_alter_pagebanner_page")]

    operations = [migrations.RunPython(update_default_copy, migrations.RunPython.noop)]
