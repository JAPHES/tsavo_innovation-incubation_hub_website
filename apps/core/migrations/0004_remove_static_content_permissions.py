from django.db import migrations


REMOVED_MODELS = (
    "achievement",
    "chairmessage",
    "corevalue",
    "focusarea",
    "program",
)


def remove_static_content_types(apps, schema_editor):
    content_type = apps.get_model("contenttypes", "ContentType")
    content_type.objects.filter(app_label="core", model__in=REMOVED_MODELS).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("core", "0003_delete_achievement_delete_chairmessage_and_more"),
    ]

    operations = [
        migrations.RunPython(remove_static_content_types, migrations.RunPython.noop),
    ]
