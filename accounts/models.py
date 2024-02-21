#accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('student', 'Student'),
        ('donor', 'Foundation Donor'),
        ('applicant', 'Scholarship Applicant'),
        ('recipient', 'Scholarship Recipient'),
        ('host', 'Auction Host'),
        ('bidder', 'Bidder'),
        ('owner', 'Local Shop Owner'),
        ('internal', 'Employee')
    )
    user_type = models.CharField(max_length=30, choices=USER_TYPES, default='student')
    is_customer = models.BooleanField(default=False, verbose_name='Customer account')
    is_admin = models.BooleanField(default=False, verbose_name='Admin account')

    class Meta:
        db_table = 'custom_user'
        swappable = 'AUTH_USER_MODEL'
        # unique_together can be uncommented if you need to enforce a unique constraint on multiple fields
        # unique_together = ('username', 'email')
