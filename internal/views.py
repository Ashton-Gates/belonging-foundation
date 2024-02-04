from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Application
from django.shortcuts import render
from .forms import InternalUserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from belonging.models import ScholarshipApplication, VendorApplication
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.urls import reverse



def internal_registration(request):
    if request.method == 'POST':
        form = InternalUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('internal:review_applications')  # Adjust the redirect as needed
    else:
        form = InternalUserCreationForm()
    return render(request, 'internal_registration.html', {'form': form})


def internal_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to an internal dashboard or home page
            return redirect('/internal/review_applications/')
        else:
            # Return an error message
            return render(request, 'internal_login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'internal_login.html')

@login_required
#@permission_required('belonging.view_application', raise_exception=True)
def review_applications(request):
    applications = Application.objects.all().order_by('-date_submitted')  # Assuming you have a submission_date field
    return render(request, 'internal/review_applications.html', {'applications': applications})


@login_required
@permission_required('belonging.view_scholarshipapplication', raise_exception=True)
def list_scholarship_applications(request):
    # Fetch all scholarship applications
    scholarship_applications = ScholarshipApplication.objects.all()
    return render(request, 'internal/scholarship_applications_list.html', {
        'scholarship_applications': scholarship_applications
    })

@login_required
@permission_required('belonging.view_vendorapplication', raise_exception=True)
def list_vendor_applications(request):
    # Fetch all vendor applications
    vendor_applications = VendorApplication.objects.all()
    return render(request, 'internal/vendor_applications_list.html', {
        'vendor_applications': vendor_applications
    })

@login_required
def get_latest_applications(request):
    scholarship_applications = ScholarshipApplication.objects.all().order_by('-id')[:10].values(
        'id', 'user_id', 'status', 'first_name', 'last_name', 'phone_number', 'email', 'date_of_birth', 'education_level', 'gender', 'business_name', 'business_description', 'video_link', 'pdf', 'question1', 'question2', 'question3'
    )
    vendor_applications = VendorApplication.objects.all().order_by('-id')[:10].values(
        'id', 'user_id', 'status', 'business_name', 'website_link', 'logo', 'question1', 'question2', 'product_suite_overview', 'partnership_outcome', 'url_api_details', 'business_proposal', 'fee_structure', 'about_me'
    )

    applications = list(scholarship_applications) + list(vendor_applications)
    return JsonResponse(applications, safe=False)

    applications = list(scholarship_applications) + list(vendor_applications)
    return JsonResponse(applications, safe=False)


