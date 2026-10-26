from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def validate_image_upload(image):
    """Limit content images to common web formats and a configurable size."""
    if Path(image.name).suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError("Upload a JPG, PNG, or WebP image.")
    if image.size > settings.MAX_IMAGE_UPLOAD_SIZE:
        limit_mb = settings.MAX_IMAGE_UPLOAD_SIZE // (1024 * 1024)
        raise ValidationError(f"Image files must be no larger than {limit_mb} MB.")

