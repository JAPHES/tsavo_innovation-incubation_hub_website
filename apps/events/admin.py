from django.contrib import admin
from django.utils.html import format_html

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ("title", "start_datetime", "venue", "image_preview", "is_published")
    list_editable = ("is_published",)
    list_filter = ("is_published", "start_datetime")
    search_fields = ("title", "description", "venue")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "start_datetime"
    ordering = ("start_datetime",)
    readonly_fields = ("image_preview",)
    fieldsets = (
        ("Event details", {"fields": ("title", "slug", "description", "venue")}),
        ("Schedule", {"fields": ("start_datetime", "end_datetime"), "description": "Only published events with a future start time appear on the homepage."}),
        ("Media and registration", {"fields": ("image", "image_preview", "registration_url")}),
        ("Publishing", {"fields": ("is_published",), "description": "Leave this unchecked while event details are being reviewed."}),
    )

    @admin.display(description="Image")
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" alt="" style="height:64px;width:112px;object-fit:cover;border-radius:7px">', obj.image.url)
        return "No image uploaded"
