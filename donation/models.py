from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class DonorAccount(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(null = True)
    address = models.TextField()
    # Additional fields for PII

class Donation(models.Model):
    donor = models.ForeignKey(DonorAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_monthly = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class OTPModel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)



    # Fields for credit card information should NOT be stored in your database due to PCI compliance
    # Instead, use a payment gateway like Stripe, PayPal, etc.