from django.shortcuts import render

from apps.core.content import SERVICES, banner_context


def service_list(request):
    context = banner_context("services")
    context["services"] = SERVICES
    return render(request, "services/list.html", context)
