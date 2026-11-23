from django.db import migrations


ORDERED_MEMBERS = (
    "Prof. Bernard Alunda",
    "Mrs Amina Ndinya",
    "Dr Rehema Swalehe",
    "Mr. Thomas Makungu",
    "Mr. Edwin Kirui",
    "Ms Belinda Owala",
    "Ms Leah Andisi",
    "Ms Anne Nyabuti",
)


def reorder_team_members(apps, schema_editor):
    members = apps.get_model("team", "TeamMember").objects.using(schema_editor.connection.alias)
    for position, name in enumerate(ORDERED_MEMBERS, start=1):
        members.filter(full_name__iexact=name).update(display_order=position)


class Migration(migrations.Migration):
    dependencies = [("team", "0006_add_chair_linkedin")]

    operations = [migrations.RunPython(reorder_team_members, migrations.RunPython.noop)]
