import re

from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError

from .models import SiteSettings


def site_context(request):
    try:
        site_settings = SiteSettings.objects.first()
    except (OperationalError, ProgrammingError):
        site_settings = None
    chair_number = site_settings.chair_whatsapp_number if site_settings else ""
    chair_whatsapp_digits = chair_number[1:] if re.fullmatch(r"\+[1-9]\d{6,14}", chair_number) else ""
    return {
        "site_settings": site_settings,
        "site_origin": settings.SITE_ORIGIN,
        "project_details_enabled": settings.PROJECT_DETAILS_ENABLED,
        "chair_whatsapp_digits": chair_whatsapp_digits,
    }
