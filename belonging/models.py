from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager



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
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    is_internal_user = models.BooleanField(default=False)

    class Meta:
        db_table = 'custom_user'
        swappable = 'AUTH_USER_MODEL'
        unique_together = ('username',) # unique_together for 'email' alone is unnecessary as 'email' is already marked unique.
class Scholarship(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    # You can add other fields like image, deadline, etc.

    def __str__(self):
        return self.title


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


from django.db import models

class PitchDeck(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # ... other fields such as file upload field, title, etc.


class ScholarshipApplication(models.Model):
    status = models.CharField(max_length=100, default='pending')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    email = models.EmailField(null=True)
    date_of_birth = models.DateField(null=True)
    education_level = models.CharField(null=True, max_length=50, choices=[
        ('high_school', 'High School'),
        ('college', 'College'),
        ('graduate_school', 'Graduate School'),
        ('blacksheep', 'Blacksheep'),
    ])
    gender = models.CharField(null=True, max_length=20, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ])
    business_name = models.CharField(max_length=200, blank=True, null=True)
    business_description = models.TextField(blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    pdf = models.FileField(upload_to='scholarship_pdfs/', blank=True, null=True)
    question1 = models.TextField(blank=True, null=True)
    question2 = models.TextField(blank=True, null=True)
    question3 = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Scholarship Application"
class VendorApplication(models.Model):
    status = models.CharField(null=True, blank=True, max_length=50, default='pending')  # Example status field
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    question1 = models.TextField(null=True, blank=True, verbose_name="Why do you want to be involved with the Belonging Foundation?")
    question2 = models.TextField(null=True, blank=True, verbose_name="How will this partnership benefit your community?")
    product_suite_overview = models.TextField(null=True, blank=True, verbose_name="Product Suite Overview")
    url_api_details = models.TextField(null=True, blank=True, verbose_name="URLs / API Details")
    partnership_outcome = models.TextField(null=True, blank=True, verbose_name="How can we ensure you get the most out of this partnership?")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='vendor_logos/', null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    website_link = models.URLField(null=True, blank=True)
    business_proposal = models.FileField(null=True, blank=True, upload_to='business_proposals/')
    fee_structure = models.FileField(upload_to='fee_structures/', null=True, blank=True)
    business_name = models.CharField(null=True, blank=True, max_length=255)  # Assuming it's a CharField
    status = models.CharField(null=True, blank=True, max_length=50, default='pending')  # Example status field
    business_desciption = models.URLField(null=True, blank=True)
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
        return self.name






    def __str__(self):
        return f'Vendor Application {self.id} by {self.user.username}'


class Venue(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    navigation_link = models.URLField(blank=True)
    social_media_link = models.URLField(blank=True)
    image = models.ImageField(upload_to='venue_images/', blank=True)

    def __str__(self):
        return self.user.username
