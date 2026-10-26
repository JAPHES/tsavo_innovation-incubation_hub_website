from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError

from .models import SiteSettings


def site_context(request):
    try:
        site_settings = SiteSettings.objects.first()
    except (OperationalError, ProgrammingError):
        site_settings = None
    return {"site_settings": site_settings, "site_origin": settings.SITE_ORIGIN}
