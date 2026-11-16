from django.db import migrations, models


def open_hydro_pellets_detail(apps, schema_editor):
    project_model = apps.get_model("projects", "InnovationProject")
    project_model.objects.using(schema_editor.connection.alias).filter(
        slug="upcycled-cotton-hydro-pellets",
    ).update(details_public=True)


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0005_innovationproject_homepage_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="innovationproject",
            name="details_public",
            field=models.BooleanField(
                default=False,
                help_text="Show the View project link and allow visitors to open this project's detail page.",
            ),
        ),
        migrations.RunPython(open_hydro_pellets_detail, migrations.RunPython.noop),
    ]
