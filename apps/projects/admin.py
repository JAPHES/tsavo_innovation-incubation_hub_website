from django.contrib import admin
from django.utils.html import format_html

from .models import InnovationProject, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 0
    fields = ("image", "alt_text", "display_order")


@admin.register(InnovationProject)
class InnovationProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "development_stage", "is_featured", "is_published", "updated_at")
    list_editable = ("is_featured", "is_published")
    list_filter = ("is_published", "is_featured", "category", "development_stage", "created_at")
    search_fields = ("title", "short_description", "full_description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at", "cover_preview")
    date_hierarchy = "created_at"
    inlines = [ProjectImageInline]
    fieldsets = (
        ("Project", {"fields": ("title", "slug", "short_description", "full_description")}),
        ("Innovation details", {"fields": ("category", "development_stage", "problem_statement", "proposed_solution", "key_features")}),
        ("Approved public information", {"fields": ("team_information", "external_url")}),
        ("Media", {"fields": ("cover_image", "cover_preview")}),
        ("Publishing", {"fields": ("is_featured", "is_published", "created_at", "updated_at")}),
    )

    @admin.display(description="Cover preview")
    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height:160px;max-width:300px;object-fit:cover">', obj.cover_image.url)
        return "No uploaded cover"
