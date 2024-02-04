from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Application

@login_required
def application_review(request):
    applications = Application.objects.all().order_by('-submission_date')  # Assuming you have a submission_date field
    return render(request, 'internal/review_applications.html', {'applications': applications})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from belonging.models import ScholarshipApplication, VendorApplication

@login_required
@permission_required('your_application_app.view_scholarshipapplication', raise_exception=True)
def list_scholarship_applications(request):
    # Fetch all scholarship applications
    scholarship_applications = ScholarshipApplication.objects.all()
    return render(request, 'internal/scholarship_applications_list.html', {
        'scholarship_applications': scholarship_applications
    })

@login_required
@permission_required('your_application_app.view_vendorapplication', raise_exception=True)
def list_vendor_applications(request):
    # Fetch all vendor applications
    vendor_applications = VendorApplication.objects.all()
    return render(request, 'internal/vendor_applications_list.html', {
        'vendor_applications': vendor_applications
    })


# Create your views here.
