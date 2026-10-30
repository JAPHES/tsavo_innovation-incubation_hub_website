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
    background_image = models.ImageField(upload_to="banners/", blank=True, max_length=500, validators=[validate_image_upload])
    image_alt_text = models.CharField(max_length=180)

    class Meta:
        ordering = ("page",)

    def __str__(self):
        return self.get_page_display()

