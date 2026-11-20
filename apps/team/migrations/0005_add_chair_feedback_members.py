from django.db import migrations


MEMBERS = (
    "Mrs Amina Ndinya",
    "Mr. Edwin Kirui",
    "Prof. Bernard Alunda",
    "Ms Belinda Owala",
    "Dr Rehema Swalehe",
    "Ms Leah Andisi",
    "Mr. Thomas Makungu",
    "Ms Anne Nyabuti",
)


def add_members_and_update_chairman(apps, schema_editor):
    database = schema_editor.connection.alias
    members = apps.get_model("team", "TeamMember").objects.using(database)

    for order, name in enumerate(MEMBERS, start=10):
        if not members.filter(full_name__iexact=name).exists():
            members.create(
                full_name=name,
                role="",
                biography="",
                display_order=order,
                is_active=True,
            )

    members.filter(
        full_name="Dr. Mwakio Mwagandi",
        role="Chair, Tsavo Innovation & Incubation Hub",
    ).update(role="Chairman, Tsavo Innovation & Incubation Hub")
    members.filter(
        full_name="Dr. Mwakio Mwagandi",
        biography=(
            "As Chair of the Tsavo Innovation & Incubation Hub, Dr. Mwakio Mwagandi "
            "welcomes students, researchers, entrepreneurs and partners to collaborate "
            "on practical innovations and sustainable ventures."
        ),
    ).update(biography=(
        "As Chairman of the Tsavo Innovation & Incubation Hub, Dr. Mwakio Mwagandi "
        "welcomes students, researchers, entrepreneurs and partners to collaborate "
        "on practical innovations and sustainable ventures."
    ))


class Migration(migrations.Migration):
    dependencies = [("team", "0004_alter_teammember_biography_alter_teammember_role")]

    operations = [migrations.RunPython(add_members_and_update_chairman, migrations.RunPython.noop)]
