from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from apps.core.content import banner_context

from .models import InnovationProject


def project_list(request):
    projects = InnovationProject.objects.filter(is_published=True)
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    stage = request.GET.get("stage", "").strip()
    if query:
        projects = projects.filter(Q(title__icontains=query) | Q(short_description__icontains=query))
    if category in InnovationProject.Category.values:
        projects = projects.filter(category=category)
    if stage in InnovationProject.Stage.values:
        projects = projects.filter(development_stage=stage)

    context = banner_context("projects")
    context.update({
        "page_obj": Paginator(projects, 9).get_page(request.GET.get("page")),
        "categories": InnovationProject.Category.choices,
        "stages": InnovationProject.Stage.choices,
        "query": query, "selected_category": category, "selected_stage": stage,
    })
    return render(request, "projects/list.html", context)


def project_detail(request, slug):
    project = get_object_or_404(InnovationProject.objects.prefetch_related("gallery"), slug=slug, is_published=True)
    return render(request, "projects/detail.html", {"project": project})
