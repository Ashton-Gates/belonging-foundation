# internal/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Application(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    application_type = models.CharField(max_length=255)  # e.g., "scholarship", "vendor"
    status = models.CharField(max_length=255)  # e.g., "pending", "approved", "denied"
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_processed = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    # In both models.py for VendorApplication and ScholarshipApplication
    status = models.CharField(max_length=255, default='pending')  # Default status


    def __str__(self):
        return f'{self.application_type} application by {self.user.username}: {self.status}'

