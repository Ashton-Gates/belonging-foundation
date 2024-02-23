# auto_deny.py

from .models import ScholarshipApplication, VendorApplication
from django.utils import timezone

def auto_deny_scholarship_applications():
    # Get all pending scholarship applications
    scholarship_applications = ScholarshipApplication.objects.filter(status='pending')
    
    for app in scholarship_applications:
        # Replace this with your actual criteria check
        if should_deny(app):
            app.status = 'denied'
            app.save()

def auto_deny_vendor_applications():
    # Get all pending vendor applications
    vendor_applications = VendorApplication.objects.filter(status='pending')
    
    for app in vendor_applications:
        # Replace this with your actual criteria check
        if should_deny(app):
            app.status = 'denied'
            app.save()

def should_deny(application):
    # Implement your criteria check here
    # For example, if the application is from a blocked region
    return application.user.region in BLOCKED_REGIONS