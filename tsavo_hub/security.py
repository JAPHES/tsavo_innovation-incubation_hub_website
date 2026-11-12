"""Browser policies for public and administrator pages."""

from ipaddress import ip_address

from django.conf import settings


def trusted_client_ip(request):
    """Use Vercel's overwritten forwarding header, never an untrusted local one."""
    if settings.IS_VERCEL:
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
        candidate = forwarded.split(",", 1)[0].strip()
        try:
            return str(ip_address(candidate))
        except ValueError:
            pass
    candidate = request.META.get("REMOTE_ADDR", "")
    try:
        return str(ip_address(candidate))
    except ValueError:
        return None


_COMMON_DIRECTIVES = (
    "default-src 'self'; base-uri 'self'; object-src 'none'; "
    "frame-ancestors 'none'; form-action 'self'; connect-src 'self'; "
    "img-src 'self' data: https://*.blob.vercel-storage.com"
)

_PUBLIC_POLICY = (
    _COMMON_DIRECTIVES
    + "; script-src 'self' https://cdn.jsdelivr.net"
    + "; style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'"
    + "; font-src 'self' data: https://cdn.jsdelivr.net"
    + "; frame-src https://www.google.com https://maps.google.com"
)

# Django admin and django-mfa currently include small inline scripts. Keep their
# policy separate so the stricter public policy does not break content editing.
_ADMIN_POLICY = (
    _COMMON_DIRECTIVES
    + "; script-src 'self' 'unsafe-inline'"
    + "; style-src 'self' 'unsafe-inline'"
    + "; font-src 'self' data:"
    + "; frame-src 'none'"
)


class PublicContentSecurityPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        admin_page = request.path.startswith(("/admin/", "/mfa/")) or request.path == "/sign-out/"
        response.setdefault("Content-Security-Policy", _ADMIN_POLICY if admin_page else _PUBLIC_POLICY)
        response.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        if admin_page:
            response["Cache-Control"] = "private, no-store"
        return response
