from datetime import timedelta
from types import SimpleNamespace

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
    SAMPLE_INNOVATIONS,
    SERVICES,
    banner_context,
)
from .models import SiteSettings


def home(request):
    featured_projects = list(
        InnovationProject.objects.filter(is_published=True, is_featured=True)[:3]
    )
    upcoming_events = list(
        Event.objects.filter(is_published=True, start_datetime__gte=timezone.now())[:3]
    )
    if not upcoming_events:
        upcoming_events = [
            SimpleNamespace(
                title="Innovation Ideation & Design Sprint",
                description="A practical session for students and emerging entrepreneurs to define problems, test ideas and shape early solution concepts.",
                venue="TIIH, Taita Taveta University",
                start_datetime=timezone.now() + timedelta(days=21),
                registration_url="",
            ),
            SimpleNamespace(
                title="Startup Readiness & Business Model Clinic",
                description="An interactive clinic focused on customer discovery, business-model refinement and preparing a clear venture pitch.",
                venue="TIIH, Taita Taveta University",
                start_datetime=timezone.now() + timedelta(days=49),
                registration_url="",
            ),
            SimpleNamespace(
                title="Innovation Pitch & Partnership Forum",
                description="A showcase connecting emerging innovators with mentors, university partners and enterprise-support networks.",
                venue="University Auditorium, Taita Taveta University",
                start_datetime=timezone.now() + timedelta(days=77),
                registration_url="",
            ),
        ]

    context = banner_context("home")
    context.update({
        "chair_message": CHAIR_MESSAGE,
        "services": SERVICES[:4],
        "featured_projects": featured_projects or SAMPLE_INNOVATIONS,
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
    lines = ["User-agent: *", "Allow: /", "Disallow: /admin/", "Disallow: /media/"]
    if request.build_absolute_uri("/"):
        lines.append(f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}")
    return HttpResponse("\n".join(lines), content_type="text/plain")


def error_404(request, exception):
    return render(request, "errors/404.html", status=404)


def error_500(request):
    return render(request, "errors/500.html", status=500)
