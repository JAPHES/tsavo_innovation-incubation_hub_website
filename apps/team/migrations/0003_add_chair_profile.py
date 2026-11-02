from django.db import migrations


CHAIR_NAME = "Dr. Mwakio Mwagandi"
CHAIR_ROLE = "Chair, Tsavo Innovation & Incubation Hub"
CHAIR_BIOGRAPHY = (
    "As Chair of the Tsavo Innovation & Incubation Hub, Dr. Mwakio Mwagandi "
    "welcomes students, researchers, entrepreneurs and partners to collaborate "
    "on practical innovations and sustainable ventures."
)


def add_chair_profile(apps, schema_editor):
    team_member = apps.get_model("team", "TeamMember")
    members = team_member.objects.using(schema_editor.connection.alias)
    chair = members.filter(full_name__iexact=CHAIR_NAME).order_by("pk").first()

    if chair is None:
        chair = members.create(
            full_name=CHAIR_NAME,
            role=CHAIR_ROLE,
            biography=CHAIR_BIOGRAPHY,
            is_chair=True,
            is_active=True,
            display_order=0,
        )
    else:
        # Preserve any existing approved biography, portrait, and LinkedIn URL.
        chair.role = CHAIR_ROLE
        chair.is_chair = True
        chair.is_active = True
        chair.display_order = 0
        chair.save(update_fields=("role", "is_chair", "is_active", "display_order"))

    members.filter(is_chair=True).exclude(pk=chair.pk).update(is_chair=False)


class Migration(migrations.Migration):
    dependencies = [
        ("team", "0002_alter_teammember_photograph"),
    ]

    operations = [
        migrations.RunPython(add_chair_profile, migrations.RunPython.noop),
    ]
