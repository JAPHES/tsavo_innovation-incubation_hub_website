from django.db import models
from django.urls import reverse

from apps.core.validators import validate_image_upload


class InnovationProject(models.Model):
    class Category(models.TextChoices):
        AGRICULTURE = "agriculture", "Agriculture"
        MINING = "mining", "Mining"
        TOURISM = "tourism", "Tourism"
        BLUE_ECONOMY = "blue-economy", "Blue Economy"
        HEALTH = "health", "Health"
        ICT = "ict", "ICT"
        EDUCATION = "education", "Education"
        BUSINESS = "business-development", "Business Development"
        OTHER = "other", "Other"

    class Stage(models.TextChoices):
        IDEA = "idea", "Idea"
        RESEARCH = "research", "Research"
        PROTOTYPE = "prototype", "Prototype"
        TESTING = "testing", "Testing"
        INCUBATION = "incubation", "Incubation"
        MARKET_READY = "market-ready", "Market Ready"

    title = models.CharField(max_length=180, db_index=True)
    slug = models.SlugField(max_length=190, unique=True)
    short_description = models.CharField(max_length=320)
    full_description = models.TextField()
    problem_statement = models.TextField(blank=True)
    proposed_solution = models.TextField(blank=True)
    category = models.CharField(max_length=40, choices=Category.choices, db_index=True)
    development_stage = models.CharField(max_length=30, choices=Stage.choices, db_index=True)
    key_features = models.TextField(blank=True, help_text="Enter one feature per line.")
    team_information = models.TextField(blank=True, help_text="Only include approved public information.")
    external_url = models.URLField(blank=True)
    cover_image = models.ImageField(upload_to="projects/", blank=True, validators=[validate_image_upload])
    is_featured = models.BooleanField(default=False, db_index=True)
    is_published = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at", "title")
        indexes = [models.Index(fields=["is_published", "is_featured", "-created_at"])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"slug": self.slug})

    @property
    def feature_list(self):
        return [item.strip() for item in self.key_features.splitlines() if item.strip()]


class ProjectImage(models.Model):
    project = models.ForeignKey(InnovationProject, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="projects/gallery/", validators=[validate_image_upload])
    alt_text = models.CharField(max_length=180)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "id")

    def __str__(self):
        return f"{self.project}: image {self.display_order + 1}"
