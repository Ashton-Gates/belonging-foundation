# belonging-foundation/belonging/models.py

from django.conf import settings
from django.db import models
from accounts.models import CustomUser

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Dashboard(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title
    
class Vendor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='belonging_vendor')
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



class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    time_zone = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    venue = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
    photo1 = models.ImageField(upload_to='events/photos/', blank=True, null=True)
    photo2 = models.ImageField(upload_to='events/photos/', blank=True, null=True)
    photo3 = models.ImageField(upload_to='events/photos/', blank=True, null=True)
    video = models.FileField(upload_to='events/videos/', blank=True, null=True)

    def __str__(self):
        return f"{self.business_name} by {self.user.username} - {self.status}"



class Venue(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    navigation_link = models.URLField(blank=True)
    social_media_link = models.URLField(blank=True)
    image = models.ImageField(upload_to='venue_images/', blank=True)

    def __str__(self):
        return self.user.username
    

