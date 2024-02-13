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
from django.http import JsonResponse



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
    # Fetch the latest applications.
    scholarship_applications = ScholarshipApplication.objects.all().order_by('-created_at')[:10]
    vendor_applications = VendorApplication.objects.all().order_by('-created_at')[:10]

    # Serialize the data for JSON response.
    applications_data = {
        'scholarship_applications': list(scholarship_applications.values()),
        'vendor_applications': list(vendor_applications.values()),
    }

    return JsonResponse(applications_data)
'''
@login_required
def get_latest_applications(request):
    # If you want to fetch applications for the logged-in user only:
    # user_applications = UserApplication.objects.filter(user=request.user)
    
    # If you want to fetch all applications for admin review:
    scholarship_applications = ScholarshipApplication.objects.all().order_by('-created_at')[:10]
    vendor_applications = VendorApplication.objects.all().order_by('-created_at')[:10]
    
    # Serialize the applications data if necessary
    scholarship_applications_data = [{
        'id': app.id,
        'user_id': app.user_id,
        'status': app.status,
        'first_name': app.first_name,
        'last_name': app.last_name,
        'phone_number': app.phone_number,
        'email': app.email,
        'date_of_birth': app.date_of_birth,
        'education_level': app.education_level,
        'gender': app.gender,
        'business_name': app.business_name,
        'business_description': app.business_description,
        'video_link': app.video_link,
        'pdf': app.pdf.url if app.pdf else None,
        'squestion1': app.squestion1,
        'squestion2': app.squestion2,
        'squestion3': app.squestion3,
        'created_at': app.created_at,
        'updated_at': app.updated_at
    } for app in scholarship_applications]

    # Serialize the vendor applications data
    vendor_applications_data = [{
        'id': app.id,
        'user_id': app.user_id,
        'status': app.status,
        'first_name': app.first_name,
        'last_name': app.last_name,
        'phone_number': app.phone_number,
        'vquestion1': app.vquestion1,
        'vquestion2': app.vquestion2,
        'product_suite_overview': app.product_suite_overview,
        'url_api_details': app.url_api_details,
        'partnership_outcome': app.partnership_outcome,
        'user': app.user.username if app.user else None,
        'business_name': app.business_name,
        'business_description': app.business_desciption,
        'logo': app.logo.url if app.logo else None,
        'website_link': app.website_link,
        'business_proposal': app.business_proposal.url if app.business_proposal else None,
        'fee_structure': app.fee_structure.url if app.fee_structure else None,
        'about_me': app.about_me,
        'created_at': app.created_at,
        'updated_at': app.updated_at
    } for app in vendor_applications]

    applications = list(scholarship_applications) + list(vendor_applications)
    return JsonResponse(applications, safe=False)

'''
