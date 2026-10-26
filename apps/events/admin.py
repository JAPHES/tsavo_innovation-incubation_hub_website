from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_datetime", "venue", "is_published")
    list_editable = ("is_published",)
    list_filter = ("is_published", "start_datetime")
    search_fields = ("title", "description", "venue")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "start_datetime"
    ordering = ("start_datetime",)
