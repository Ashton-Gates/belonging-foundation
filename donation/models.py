#donation/models.py

from django.db import models
from django.db.models import Q
from django.conf import settings
from djstripe.models import StripeModel
from django.contrib.auth.models import User


class DonorAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True ,related_name='donor_account')    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(null = True)
    address = models.TextField()
    # Additional fields for PII


    def __str__(self):
        return self.user.username

class Payment(StripeModel):
    djstripe_owner_account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='donation_payments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_user')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'description', 'amount'],
                condition=Q(paid=True),
                name='unique_paid_payments'
            )
        ]
    
    def __str__(self):
        return f'{self.user.username} - {self.description}'    


class OTPModel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)



    # Fields for credit card information should NOT be stored in your database due to PCI compliance
    # Instead, use a payment gateway like Stripe, PayPal, etc.