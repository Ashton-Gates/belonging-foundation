#applicant/views.py
from datetime import timezone
import os
from reportlab.pdfgen import canvas
from django.conf import settings
from referee.models import Referee
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from django.views.decorators.http import require_GET
from django.core.files.storage import FileSystemStorage
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, FileResponse, JsonResponse
from .models import PitchDeck, ScholarshipApplication, VendorApplication, Scholarship, UserApplication
from .forms import ApplicantRegistrationForm, ApplicantLoginForm, VendorApplicationForm, ScholarshipApplicationForm
from .auto_deny import auto_deny_scholarship_applications, auto_deny_vendor_applications


@login_required
def scholar_landing(request):
    return render(request, 'applicant/scholar_landing.html')

@login_required
def vendor_landing(request):
    return render(request, 'applicant/vendor_landing.html')

@login_required
def get_latest_applications(request):
    scholarship_applications = ScholarshipApplication.objects.filter(user=request.user).order_by('-created_at')[:10].values(
        'id', 'user_id', 'status', 'first_name', 'last_name', 'phone_number', 'email', 
        'date_of_birth', 'education_level', 'gender', 'business_name', 'business_description', 
        'video_link', 'pdf', 'squestion1', 'squestion2', 'squestion3', 'created_at', 'updated_at'
    )

    vendor_applications = VendorApplication.objects.filter(user=request.user).order_by('-created_at')[:10].values(
        'id', 'user_id', 'status', 'business_name', 'website_link', 'logo', 'business_proposal', 'fee_structure', 
        'about_me', 'vquestion1', 'vquestion2', 'product_suite_overview', 'partnership_outcome', 'url_api_details', 'created_at', 'updated_at'
    )

def registration(request):
    if request.method == 'POST':
        form = ApplicantRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('applicant_dashboard')
    else:
        form = ApplicantRegistrationForm()
    return render(request, 'applicant/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = ApplicantLoginForm(request=request, data=request.POST)
        username = request.POST.get('email')
        password = request.POST.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Check application status
            scholarship_apps = ScholarshipApplication.objects.filter(user=user, status='approved')
            if scholarship_apps.exists():
                # Redirect to recipient dashboard if there's at least one approved application
                return redirect('recipient_dashboard')
            
            vendor_apps = VendorApplication.objects.filter(user=user, status='approved')
            if vendor_apps.exists():
                # Redirect to vendor dashboard if there's at least one approved application
                return redirect('vendor_dashboard')
            
            # Default to applicant dashboard if no approved applications
            return redirect('applicant_dashboard')
        else:
            return render(request, 'applicant/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = ApplicantRegistrationForm()
        return render(request, 'applicant/login.html', {'form': form})
    
@login_required
def applicant_dashboard(request):
    user = request.user  # Get the logged-in user

    # Fetch the latest applications
    latest_scholarship_application = ScholarshipApplication.objects.filter(user=user).order_by('-created_at').first()
    latest_vendor_application = VendorApplication.objects.filter(user=user).order_by('-created_at').first()

    # Assuming UserApplication is correctly set up to link to the user's applications
    user_applications = UserApplication.objects.filter(user=user).prefetch_related('scholarship_applications', 'vendor_applications').first()

    # Fetch all applications related to the user sorted by created_at
    scholarship_applications = user_applications.scholarship_applications.all().order_by('-created_at') if user_applications else []
    vendor_applications = user_applications.vendor_applications.all().order_by('-created_at') if user_applications else []

    # Fetch all scholarships for display
    scholarships = Scholarship.objects.all()

    # Fetch user's pitch decks
    user_pitch_decks = PitchDeck.objects.filter(user=user)

    context = {
        'latest_scholarship_application': latest_scholarship_application,
        'latest_vendor_application': latest_vendor_application,
        'scholarship_applications': scholarship_applications,
        'vendor_applications': vendor_applications,
        'scholarships': scholarships,
        'user_pitch_decks': user_pitch_decks,
    }

    return render(request, 'applicant/applicant_dashboard.html', context)

@login_required
def scholarship_application(request):
        # When you want to auto-deny applications, just call the function
    auto_deny_scholarship_applications()

    if request.method == "POST":
        form = ScholarshipApplicationForm(request.POST, request.FILES)
        existing_app = ScholarshipApplication.objects.filter(user=request.user).exists()
        if existing_app:
            messages.error(request, 'You have already submitted an application.')
            return redirect('applicant_dashboard')
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user  # Set the user to the current logged-in user
            application.status = 'pending'  # Explicitly set status if not defaulting in the model
            application.save()
            messages.success(request, "Your scholarship application has been successfully submitted.")
            return redirect('applicant_dashboard')
        else:
            # If the form is not valid, render the form again with errors
            messages.error(request, "There was an error with your submission.")
            
    else:
        form = ScholarshipApplicationForm()  # Instantiate a new form for a GET request

    # Render the form with messages if they exist
    return render(request, 'belonging/scholarship_app.html', {'form': form})

@login_required
def vendor_application(request):
        # When you want to auto-deny applications, just call the function
    auto_deny_vendor_applications()
    if request.method == 'POST':
        form = VendorApplicationForm(request.POST, request.FILES)
        existing_vendor_app = VendorApplication.objects.filter(user=request.user).exists()
        if existing_vendor_app:
            messages.error(request, 'You have already submitted a vendor application.')
            return redirect('applicant_dashboard')
        if form.is_valid():
            vendor_application = form.save(commit=False)
            vendor_application.user = request.user
            vendor_application.status = 'pending'
            vendor_application.save()
            messages.success(request, 'Your vendor application has been successfully submitted.')
            return redirect('applicant_dashboard')
        else:
            messages.error(request, 'There was an error with your submission: ' + ', '.join(form.errors))
    else:
        form = VendorApplicationForm()

    return render(request, 'belonging/vendor_app.html', {'form': form})



@login_required
def download_scholarship_pdf(request, application_id):
    application = ScholarshipApplication.objects.get(id=application_id, user=request.user)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Scholarship_Application_{application_id}.pdf"'
    
    p = canvas.Canvas(response)
    y = 800  # Start from the top of the page.
    x = 50   # Margin from the left.

    # Adjust the line height as needed
    line_height = 14

    # Draw each field.
    fields = [
        f"First Name: {application.first_name}",
        f"Last Name: {application.last_name}",
        f"Phone Number: {application.phone_number}",
        f"Email: {application.email}",
        f"Date of Birth: {application.date_of_birth.strftime('%Y-%m-%d') if application.date_of_birth else 'N/A'}",
        f"Education Level: {application.get_education_level_display()}",
        f"Gender: {application.get_gender_display()}",
        f"Business Name: {application.business_name}",
        f"Business Description: {application.business_description}",
        f"Video Link: {application.video_link}",
        # For the PDF field, you might want to display a message rather than the URL
        "PDF: Attached",
        f"SQuestion1: {application.squestion1}",
        f"SQuestion2: {application.squestion2}",
        f"SQuestion3: {application.squestion3}",
    ]

    for field in fields:
        p.drawString(x, y, field)
        y -= line_height  # Move down for the next line.

    p.showPage()
    p.save()
    return response

@login_required
def download_vendor_pdf(request, application_id):
    application = VendorApplication.objects.get(id=application_id, user=request.user)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Vendor_Application_{application_id}.pdf"'
    
    p = canvas.Canvas(response)
    y = 800  # Start from the top of the page for text.
    y_image = 650  # Start position for the image.
    x = 50   # Margin from the left for text.
    x_image = 50  # Margin from the left for the image.

    # Adjust the line height as needed
    line_height = 14

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter  # Get the dimensions of the page
    y = height - 50  # Start from the top of the page for text
    x_text = 300  # X position for text, assuming the image is on the left side

        # Draw the logo
    if application.logo:
        logo_path = os.path.join(settings.MEDIA_ROOT, application.logo.name)
        logo_height = 100  # Or calculate the height based on the width to maintain aspect ratio
        logo_width = 200  # Adjust as necessary
        x_image = 50  # Margin from the left for the image
        y_image = height - 50 - logo_height  # Position the top of the image at the same y as text
        p.drawImage(logo_path, x_image, y_image, width=logo_width, height=logo_height, mask='auto')

    # Adjust the y position for text start after the image
    y_text_start = y_image - 15  # Start the text below the image

    # Draw each field.
    fields = [
        f"Logo: Attached",
        f"First Name: {application.first_name}",
        f"Last Name: {application.last_name}",
        f"Phone Number: {application.phone_number}",
        f"VQuestion1: {application.vquestion1}",
        f"VQuestion2: {application.vquestion2}",
        f"Product Suite Overview: {application.product_suite_overview}",
        f"URL/API Details: {application.url_api_details}",
        f"Partnership Outcome: {application.partnership_outcome}",
        f"Business Name: {application.business_name}",
        f"Business Description: {application.business_desciption}",
        f"Website Link: {application.website_link}",        
        f"Business Proposal: " + (application.business_proposal.name if application.business_proposal else "Not provided"),
        "Fee Structure: " + (application.fee_structure.name if application.fee_structure else "Not provided"),
    ]


        # Check if the logo exists and draw it.
    if application.logo:
        logo_path = os.path.join(settings.MEDIA_ROOT, application.logo.name)
        p.drawImage(logo_path, x_image, y_image, width=200, height=100, mask='auto')  # You may need to adjust the width and height.

        # Draw the text fields below the image
    for field in fields:
        p.drawString(x_text, y_text_start, field)
        y_text_start -= line_height  # Move down for the next line

    p.showPage()
    p.save()
    return response

@login_required
def withdraw_application(request, application_id):
    application = get_object_or_404(ScholarshipApplication, id=application_id, user=request.user)
    scholarship = application.scholarship  # Assuming a ForeignKey relationship to Scholarship

    if timezone.now() < scholarship.deadline:
        application.status = 'withdrawn'  # Set to 'withdrawn' or similar
        application.save()
        messages.success(request, "Your application has been successfully withdrawn.")
    else:
        messages.error(request, "The deadline has passed; the application cannot be withdrawn.")

    return redirect('some-view-name')  # Redirect to an appropriate page

@require_GET
def validate_referee_id(request):
    referee_id = request.GET.get('referee_id', None)
    data = {
        'is_valid': Referee.objects.filter(referee_id=referee_id).exists()
    }
    return JsonResponse(data)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    # Log out the user.
    logout(request)
    # Redirect to login page.
    return redirect('applicant:login')

@login_required
def delete_account(request):
    if request.method == 'POST':
        # Delete the user's account
        request.user.delete()
        logout(request)
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home')  # Redirect to the homepage or a goodbye page

    return render(request, 'belonging/delete_account.html')  # Confirm account deletion page

