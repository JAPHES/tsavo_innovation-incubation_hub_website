from django.db import models


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=140)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    subject = models.CharField(max_length=180)
    message = models.TextField(max_length=4000)
    consent = models.BooleanField()
    submitted_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_read = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ("-submitted_at",)
        permissions = [("export_contactmessage", "Can export contact messages")]

    def __str__(self):
        return f"{self.subject} — {self.full_name}"
