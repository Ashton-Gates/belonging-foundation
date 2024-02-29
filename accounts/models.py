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
        ('internal', 'Employee'),
        ('vendor', 'Vendor'),
        ('sponsor', 'Sponsor'),
        ('distributor', 'Account Distributor'),
        ('venue', 'Venue'),
        ('other', 'Other')
    )
    user_type = models.CharField(max_length=30, choices=USER_TYPES, default='other')
    is_customer = models.BooleanField(default=False, verbose_name='Customer account')
    is_admin = models.BooleanField(default=False, verbose_name='Admin account')
    company = models.CharField(max_length=255, blank=True, null=True, verbose_name='Company Name')
    ecommerce_website = models.URLField(max_length=255, blank=True, verbose_name='eCommerce Website')
    profile_website = models.URLField(max_length=255, blank=True, verbose_name='Profile Website')
    instagram_link = models.URLField(max_length=255, blank=True, verbose_name='Instagram')
    facebook_link = models.URLField(max_length=255, blank=True, verbose_name='Facebook')



    class Meta:
        db_table = 'custom_user'
        swappable = 'AUTH_USER_MODEL'
        # unique_together can be uncommented if you need to enforce a unique constraint on multiple fields
        # unique_together = ('username', 'email')
