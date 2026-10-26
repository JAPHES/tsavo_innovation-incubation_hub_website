from django.db import models

from apps.core.validators import validate_image_upload


class TeamMember(models.Model):
    full_name = models.CharField(max_length=160)
    role = models.CharField(max_length=140)
    biography = models.TextField(max_length=1200)
    photograph = models.ImageField(upload_to="team/", blank=True, validators=[validate_image_upload])
    display_order = models.PositiveSmallIntegerField(default=0)
    is_chair = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    email = models.EmailField(blank=True, help_text="Publish only with the member's approval.")
    linkedin_url = models.URLField(blank=True)

    class Meta:
        ordering = ("-is_chair", "display_order", "full_name")

    def __str__(self):
        return f"{self.full_name} — {self.role}"
