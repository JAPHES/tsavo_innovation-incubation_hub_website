from django.shortcuts import render

from apps.core.content import banner_context

from .models import TeamMember


def team_list(request):
    context = banner_context("team")
    members = TeamMember.objects.filter(is_active=True)
    context.update({"chair": members.filter(is_chair=True).first(), "members": members.filter(is_chair=False)})
    return render(request, "team/list.html", context)
