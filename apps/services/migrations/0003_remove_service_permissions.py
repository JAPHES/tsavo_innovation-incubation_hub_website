from django.db import migrations


def remove_service_content_type(apps, schema_editor):
    content_type = apps.get_model("contenttypes", "ContentType")
    content_type.objects.filter(app_label="services", model="service").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("services", "0002_delete_service"),
    ]

    operations = [
        migrations.RunPython(remove_service_content_type, migrations.RunPython.noop),
    ]
