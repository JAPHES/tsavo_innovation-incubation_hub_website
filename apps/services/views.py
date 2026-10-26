from django.shortcuts import render

from apps.core.content import banner_context

from .models import Service


def service_list(request):
    context = banner_context("services")
    context["services"] = Service.objects.filter(is_published=True)
    return render(request, "services/list.html", context)
