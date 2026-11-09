from django.shortcuts import render
from django.views.decorators.http import require_GET

from apps.core.content import banner_context


@require_GET
def contact(request):
    return render(request, "contact/contact.html", banner_context("contact"))
