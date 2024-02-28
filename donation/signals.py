from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DonorAccount, Payment

@receiver(post_save, sender=Payment)
def update_donor_account(sender, instance, created, **kwargs):
    if created:  # Only run on the creation of a new payment
        # Assuming `DonorAccount` is related to `Payment` via `user`
        # and `DonorAccount` has a `user` ForeignKey to `settings.AUTH_USER_MODEL`
        donor_account = DonorAccount.objects.filter(user=instance.user).first()
        if donor_account:
            # Update donor_account fields here
            donor_account.save()
