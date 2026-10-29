from django.core.exceptions import ValidationError
from django.db import models

from apps.core.validators import validate_image_upload


class Event(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=190, unique=True)
    description = models.TextField(max_length=1200)
    venue = models.CharField(max_length=220)
    start_datetime = models.DateTimeField(db_index=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to="events/", blank=True, max_length=500, validators=[validate_image_upload])
    registration_url = models.URLField(blank=True)
    is_published = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ("start_datetime", "title")
        indexes = [models.Index(fields=["is_published", "start_datetime"])]

    def clean(self):
        if self.end_datetime and self.end_datetime < self.start_datetime:
            raise ValidationError({"end_datetime": "End time cannot precede start time."})

    def __str__(self):
        return self.title
