from django.db import models
from django.urls import reverse


class Service(models.Model):
    name = models.CharField(max_length=140, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(max_length=1200)
    icon = models.CharField(max_length=60, default="bi-lightbulb")
    display_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ("display_order", "name")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"{reverse('services:list')}#{self.slug}"
