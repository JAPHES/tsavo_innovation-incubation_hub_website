from django.core.exceptions import ValidationError
from django.db import models

from .validators import validate_image_upload


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("This record is required and cannot be deleted.")


class SiteSettings(SingletonModel):
    website_name = models.CharField(max_length=160, default="Tsavo Innovation & Incubation Hub")
    abbreviation = models.CharField(max_length=20, default="TIIH")
    tagline = models.CharField(max_length=120, default="Cultivating Entrepreneurs")
    contact_email = models.EmailField(default="tiih@ttu.ac.ke")
    contact_phone = models.CharField(max_length=40, default="+254 722 274257")
    description = models.TextField(max_length=500)
    vision = models.TextField()
    mission = models.TextField()
    main_objective = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    map_embed_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    x_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "site settings"
        verbose_name_plural = "site settings"

    def __str__(self):
        return self.website_name


class PageBanner(models.Model):
    PAGE_CHOICES = [("home", "Home"), ("about", "About Us"), ("services", "Our Services"),
                    ("projects", "Innovation Projects"), ("team", "Our Team"), ("contact", "Contact Us")]
    page = models.CharField(max_length=20, choices=PAGE_CHOICES, unique=True)
    heading = models.CharField(max_length=160)
    supporting_text = models.CharField(max_length=280)
    background_image = models.ImageField(upload_to="banners/", blank=True, validators=[validate_image_upload])
    image_alt_text = models.CharField(max_length=180)

    class Meta:
        ordering = ("page",)

    def __str__(self):
        return self.get_page_display()


class ChairMessage(SingletonModel):
    chair_name = models.CharField(max_length=160, blank=True)
    official_position = models.CharField(max_length=160, default="Hub Chair")
    photograph = models.ImageField(upload_to="team/", blank=True, validators=[validate_image_upload])
    message = models.TextField()
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Chair's message"
        verbose_name_plural = "Chair's message"

    def __str__(self):
        return self.chair_name or "Chair's message"


class CoreValue(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=240)
    icon = models.CharField(max_length=60, default="bi-gem")
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "name")

    def __str__(self):
        return self.name


class FocusArea(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.CharField(max_length=300)
    icon = models.CharField(max_length=60, default="bi-lightbulb")
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "name")

    def __str__(self):
        return self.name


class Program(models.Model):
    title = models.CharField(max_length=160, unique=True)
    description = models.TextField(max_length=800)
    image = models.ImageField(upload_to="programs/", blank=True, validators=[validate_image_upload])
    icon = models.CharField(max_length=60, default="bi-rocket-takeoff")
    is_published = models.BooleanField(default=False, db_index=True)
    application_url = models.URLField(blank=True)
    opening_date = models.DateField(blank=True, null=True)
    closing_date = models.DateField(blank=True, null=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "title")

    def clean(self):
        if self.opening_date and self.closing_date and self.closing_date < self.opening_date:
            raise ValidationError({"closing_date": "Closing date cannot precede opening date."})

    def __str__(self):
        return self.title


class Achievement(models.Model):
    title = models.CharField(max_length=180)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to="achievements/", blank=True, validators=[validate_image_upload])
    achievement_date = models.DateField(blank=True, null=True)
    is_published = models.BooleanField(default=False, db_index=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "-achievement_date", "title")

    def __str__(self):
        return self.title

