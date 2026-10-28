from datetime import timedelta
from types import SimpleNamespace

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from apps.events.models import Event
from apps.projects.models import InnovationProject
from apps.services.models import Service

from .content import SAMPLE_INNOVATIONS, banner_context
from .models import ChairMessage, CoreValue, FocusArea, Program, SiteSettings


def home(request):
    featured_projects = list(
        InnovationProject.objects.filter(is_published=True, is_featured=True)[:3]
    )
    upcoming_events = list(
        Event.objects.filter(is_published=True, start_datetime__gte=timezone.now())[:2]
    )
    events_are_examples = not upcoming_events
    if events_are_examples:
        upcoming_events = [
            SimpleNamespace(
                preview_only=True,
                title="Innovation Ideation & Design Sprint",
                description="A practical session for students and emerging entrepreneurs to define problems, test ideas and shape early solution concepts.",
                venue="TIIH, Taita Taveta University",
                start_datetime=timezone.now() + timedelta(days=21),
                registration_url="",
            ),
            SimpleNamespace(
                preview_only=True,
                title="Startup Readiness & Business Model Clinic",
                description="An interactive clinic focused on customer discovery, business-model refinement and preparing a clear venture pitch.",
                venue="TIIH, Taita Taveta University",
                start_datetime=timezone.now() + timedelta(days=49),
                registration_url="",
            ),
        ]

    context = banner_context("home")
    context.update({
        "chair_message": ChairMessage.objects.filter(is_published=True).first(),
        "services": Service.objects.filter(is_published=True)[:4],
        "featured_projects": featured_projects or SAMPLE_INNOVATIONS,
        "innovations_are_examples": not featured_projects,
        "programs": Program.objects.filter(is_published=True)[:4],
        "upcoming_events": upcoming_events,
        "events_are_examples": events_are_examples,
    })
    return render(request, "core/home.html", context)


def about(request):
    context = banner_context("about")
    context.update({
        "settings_record": SiteSettings.objects.first(),
        "core_values": CoreValue.objects.all(),
        "focus_areas": FocusArea.objects.all(),
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
