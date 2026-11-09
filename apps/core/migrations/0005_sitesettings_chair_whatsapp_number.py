from django.core.validators import RegexValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_remove_static_content_permissions"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="chair_whatsapp_number",
            field=models.CharField(
                max_length=16,
                blank=True,
                default="+254722274257",
                validators=[RegexValidator(r"^\+[1-9]\d{6,14}$", "Use international format, such as +254722274257.")],
                help_text="Public WhatsApp number for the hub chair. Clear it to hide the floating button.",
            ),
        ),
    ]
