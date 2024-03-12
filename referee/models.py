# belonging-foundation/referee/models.py

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from accounts.models import CustomUser



class SponsorApplication(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sponsor_application'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    why_sponsor = models.TextField(verbose_name="Why do you want to be a sponsor?")
    qualifications = models.TextField()
    approved = models.BooleanField(default=False)
    rejection_feedback = models.TextField(blank=True, null=True)
    referee = models.OneToOneField('Referee', on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {'Approved' if self.approved else 'Pending'}"
    
class Referee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,

    )
    referee_id = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.referee_id})"

class Scholarship(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

class Referral(models.Model):
    '''@staticmethod
    def default_scholarship_id():
        scholarship = Scholarship.objects.first()
        return scholarship.id if scholarship else None'''

    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='referee_profile', null=True)
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, null=True)
    nominee_name = models.CharField(max_length=255)
    nominee_email = models.EmailField()
    nominee_phone_number = models.CharField(max_length=20, blank=True, null=True)
    justification = models.TextField()
    referee = models.ForeignKey(Referee, on_delete=models.CASCADE)

    @property
    def scholarship_info(self):
        return {
            'title': self.scholarship.title,
            'description': self.scholarship.description,
            'grand_prize': self.scholarship.grand_prize,

        }


def __str__(self):
    if self.user is None:
        return f"User is None ({self.referee_id})"
    return f"{self.user.username} ({self.referee_id})"
