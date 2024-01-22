from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
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
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')

    class Meta:
        db_table = 'custom_user'
        swappable = 'AUTH_USER_MODEL'
        unique_together = ('email',)


    # Additional fields can be added here, if needed
class Dashboard(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title
    


#Silent Auction Capabilities
    
class Vendor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Additional vendor-specific fields

class Bidder(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Additional bidder-specific fields

class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images/')  # Ensure you have Pillow installed

    def __str__(self):
        return self.name
    
class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    bidder = models.ForeignKey(Bidder, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)