from django.shortcuts import render

from apps.core.content import banner_context

from .models import TeamMember


def team_list(request):
    context = banner_context("team")
    context["members"] = list(TeamMember.objects.filter(is_active=True))
    return render(request, "team/list.html", context)
