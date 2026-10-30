from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.utils.html import format_html

from .models import Achievement, ChairMessage, CoreValue, FocusArea, PageBanner, Program, SiteSettings


class TIIHAdminAuthenticationForm(AdminAuthenticationForm):
    """Admin authentication with explicit session persistence control."""

    remember_me = forms.BooleanField(required=False, label="Remember me")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.pop("autofocus", None)

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if self.request is not None:
            expiry = settings.SESSION_COOKIE_AGE if self.cleaned_data.get("remember_me") else 0
            self.request.session.set_expiry(expiry)


admin.site.login_form = TIIHAdminAuthenticationForm


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ("Identity", {"fields": ("website_name", "abbreviation", "tagline", "description")}),
        ("Official content", {"fields": ("vision", "mission", "main_objective")}),
        ("Contact", {"fields": ("contact_email", "contact_phone", "location", "map_embed_url")}),
        ("Verified social profiles", {"fields": ("facebook_url", "linkedin_url", "x_url", "youtube_url")}),
    )


@admin.register(PageBanner)
class PageBannerAdmin(admin.ModelAdmin):
    list_display = ("page", "heading", "image_preview")
    search_fields = ("heading", "supporting_text")
    ordering = ("page",)

    @admin.display(description="Image")
    def image_preview(self, obj):
        if obj.background_image:
            return format_html('<img src="{}" style="height:48px;width:90px;object-fit:cover;border-radius:4px">', obj.background_image.url)
        return "Static fallback"


@admin.register(ChairMessage)
class ChairMessageAdmin(SingletonAdmin):
    list_display = ("__str__", "official_position", "is_published", "updated_at")
    readonly_fields = ("updated_at",)


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order", "icon")
    list_editable = ("display_order",)
    search_fields = ("name", "description")


@admin.register(FocusArea)
class FocusAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order", "icon")
    list_editable = ("display_order",)
    search_fields = ("name", "description")


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "opening_date", "closing_date", "display_order")
    list_editable = ("is_published", "display_order")
    list_filter = ("is_published", "opening_date", "closing_date")
    search_fields = ("title", "description")


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("title", "achievement_date", "is_published", "display_order")
    list_editable = ("is_published", "display_order")
    list_filter = ("is_published", "achievement_date")
    search_fields = ("title", "description")
