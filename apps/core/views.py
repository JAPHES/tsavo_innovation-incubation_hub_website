from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from apps.events.models import Event
from apps.projects.models import InnovationProject
from apps.services.models import Service

from .content import banner_context
from .models import Achievement, ChairMessage, CoreValue, FocusArea, Program, SiteSettings


def home(request):
    context = banner_context("home")
    context.update({
        "chair_message": ChairMessage.objects.filter(is_published=True).first(),
        "services": Service.objects.filter(is_published=True)[:4],
        "featured_projects": InnovationProject.objects.filter(is_published=True, is_featured=True)[:4],
        "programs": Program.objects.filter(is_published=True)[:5],
        "upcoming_events": Event.objects.filter(is_published=True, start_datetime__gte=timezone.now())[:3],
        "achievements": Achievement.objects.filter(is_published=True)[:3],
        "focus_areas": FocusArea.objects.all()[:6],
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
