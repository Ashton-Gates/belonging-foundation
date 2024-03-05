#applicant/models.py

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# Model to track login events for applicants
class ApplicantLogin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    # You can add additional fields like IP address, user agent, etc.

    def __str__(self):
        return f"{self.user.username} logged in at {self.timestamp}"

# Model to track registration events for applicants
class ApplicantRegistration(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    # You can add additional fields like the source of registration, referral info, etc.

    def __str__(self):
        return f"{self.user.username} registered at {self.timestamp}"
    
# Model to track scholarship events for applicants
class Scholarship(models.Model):
    title = models.CharField(max_length=200)
    grand_prize = models.CharField(max_length=200, null=True, blank=True)
    second_prize = models.CharField(max_length=200, null=True, blank=True)
    third_place = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    deadline = models.DateTimeField(null=True, blank=True)
    # You can add other fields like image, deadline, etc.

    def __str__(self):
        return self.title
    
    # Additional fields can be added here, if needed
class Dashboard(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title
    
class ScholarshipApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, default=False)
    denial_feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=100, default='pending')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)    
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
    squestion1 = models.TextField(blank=True, null=True)
    squestion2 = models.TextField(blank=True, null=True)
    squestion3 = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Scholarship Application"
class VendorApplication(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vendor_applications'
    )
    denial_feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(null=True, blank=True, max_length=50, default='pending')  # Example status field
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    vquestion1 = models.TextField(null=True, blank=True, verbose_name="Why do you want to be involved with the Belonging Foundation?")
    vquestion2 = models.TextField(null=True, blank=True, verbose_name="How will this partnership benefit your community?")
    product_suite_overview = models.TextField(null=True, blank=True, verbose_name="Product Suite Overview")
    url_api_details = models.TextField(null=True, blank=True, verbose_name="URLs / API Details")
    partnership_outcome = models.TextField(null=True, blank=True, verbose_name="How can we ensure you get the most out of this partnership?")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    logo = models.ImageField(upload_to='vendor_logos/', null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    website_link = models.URLField(null=True, blank=True)
    business_proposal = models.FileField(null=True, blank=True, upload_to='business_proposals/')
    fee_structure = models.FileField(upload_to='fee_structures/', null=True, blank=True)
    business_name = models.CharField(null=True, blank=True, max_length=255)  # Assuming it's a CharField
    status = models.CharField(null=True, blank=True, max_length=50, default='pending')  # Example status field
    business_desciption = models.TextField(null=True, blank=True, verbose_name="Brief description of your business")

    def __str__(self):
        return f'Vendor Application {self.id} by {self.user.username}'
    
class PitchDeck(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pitch_deck = models.FileField(upload_to='pitch_decks/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Pitch Deck"
    
class UserApplication(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_applications")
    scholarship_applications = models.ManyToManyField('ScholarshipApplication', blank=True)
    vendor_applications = models.ManyToManyField('VendorApplication', blank=True)
    # Include other application types as needed

    def __str__(self):
        return f"Applications for {self.user.username}"

    @property
    def all_applications(self):
        # This method aggregates all applications related to the user across different types
        applications = []
        applications.extend(list(self.scholarship_applications.all()))
        applications.extend(list(self.vendor_applications.all()))
        # Extend with other application types as needed
        return applications