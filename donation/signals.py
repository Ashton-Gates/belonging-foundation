from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Donation, DonorAccount

@receiver(post_save, sender=Donation)
def update_donor_account(sender, instance, created, **kwargs):
    if created:  # Only run on the creation of a new donation
        donor_account = instance.donor
        donor_account.first_name = instance.first_name
        donor_account.last_name = instance.last_name
        donor_account.phone_number = instance.phone_number
        donor_account.address = instance.address
        donor_account.save()
