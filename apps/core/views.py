from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from apps.events.models import Event
from apps.projects.models import InnovationProject

from .content import (
    CHAIR_MESSAGE,
    CORE_VALUES,
    FOCUS_AREAS,
    PROGRAMS,
    SERVICES,
    banner_context,
)
from .models import SiteSettings


def home(request):
    featured_projects = list(
        InnovationProject.objects.filter(is_published=True, is_featured=True).order_by("homepage_order", "-created_at")[:3]
    )
    upcoming_events = list(
        Event.objects.filter(is_published=True, start_datetime__gte=timezone.now())[:3]
    )

    context = banner_context("home")
    context.update({
        "chair_message": CHAIR_MESSAGE,
        "services": SERVICES[:4],
        "featured_projects": featured_projects,
        "programs": PROGRAMS[:4],
        "upcoming_events": upcoming_events,
    })
    return render(request, "core/home.html", context)


def about(request):
    context = banner_context("about")
    context.update({
        "settings_record": SiteSettings.objects.first(),
        "core_values": CORE_VALUES,
        "focus_areas": FOCUS_AREAS,
    })
    return render(request, "core/about.html", context)


def robots_txt(request):
    lines = [
        "User-agent: *", "Allow: /", "Disallow: /admin/", "Disallow: /media/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def error_404(request, exception):
    return render(request, "errors/404.html", status=404)


def error_500(request):
    return render(request, "errors/500.html", status=500)
