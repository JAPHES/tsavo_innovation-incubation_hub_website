from django.contrib import admin

from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "role", "is_chair", "is_active", "display_order")
    list_editable = ("is_chair", "is_active", "display_order")
    list_filter = ("is_active", "is_chair")
    search_fields = ("full_name", "role", "biography")
    ordering = ("-is_chair", "display_order", "full_name")
    fieldsets = (
        ("Profile", {"fields": ("full_name", "role", "biography", "photograph")}),
        ("Page placement", {"fields": ("is_chair", "is_active", "display_order")}),
        (
            "Public contact and LinkedIn profile",
            {
                "fields": ("linkedin_url", "email"),
                "description": "Add a verified public LinkedIn profile URL when available and approved.",
            },
        ),
    )
