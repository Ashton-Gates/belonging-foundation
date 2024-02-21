from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

class VenueLogin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    login_ip = models.CharField(max_length=45)  # IPv4 and IPv6 compatibility

    def __str__(self):
        return f"{self.user.username} logged in at {self.login_time}"
    
class VenueRegister(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    business_email = models.EmailField(unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name    
    
class VenueUserData(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_email = models.EmailField(
        unique=True,
        validators=[RegexValidator(regex='^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        message='Please enter a valid business email address.', code='invalid_email')]
    )
    business_name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    website = models.URLField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.business_name} - {self.business_email}"