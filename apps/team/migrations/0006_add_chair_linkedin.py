from django.db import migrations


CHAIR_LINKEDIN_URL = "https://www.linkedin.com/in/dr-mwakio-wa-mwagandi-phd-34b20119/"


def set_chair_linkedin_if_blank(apps, schema_editor):
    members = apps.get_model("team", "TeamMember").objects.using(schema_editor.connection.alias)
    members.filter(full_name="Dr. Mwakio Mwagandi", linkedin_url="").update(
        linkedin_url=CHAIR_LINKEDIN_URL
    )


class Migration(migrations.Migration):
    dependencies = [("team", "0005_add_chair_feedback_members")]

    operations = [migrations.RunPython(set_chair_linkedin_if_blank, migrations.RunPython.noop)]
