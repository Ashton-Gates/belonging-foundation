from django.db import models
from django.conf import settings

class Vendor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_vendor')
    business_name = models.CharField(max_length=255, blank=True)
    business_description = models.TextField(blank=True, verbose_name="Brief description of your business")
    website_link = models.URLField(blank=True)
    logo = models.ImageField(upload_to='vendor_logos/', blank=True)
    # Other vendor-specific fields

    def __str__(self):
        return self.business_name or self.user.username
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    # Add other relevant fields and methods

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    # Add other relevant fields and methods
    def __str__(self):
        return self.name


# Create your models here.
class Item(models.Model):
    CONDITION_CHOICES = (
        ('new', 'New'),
        ('poor', 'Poor'),
        ('fair', 'Fair'),
        ('good', 'Good'),
        ('excellent', 'Excellent')
        # Add other condition options
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images/')  # Add this line for the image field
    purchased_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    purchased_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
