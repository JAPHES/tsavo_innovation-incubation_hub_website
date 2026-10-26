from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "full_name", "email", "submitted_at", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read", "submitted_at", "consent")
    search_fields = ("full_name", "email", "subject", "message")
    readonly_fields = ("full_name", "email", "phone", "subject", "message", "consent", "submitted_at")
    date_hierarchy = "submitted_at"

    def has_add_permission(self, request):
        return False
