# views.py
import csv
import os
import requests
from django.conf import settings
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.core.mail import EmailMessage
from .forms import CustomUserCreationForm, CustomAuthenticationForm, VendorApplicationForm, ScholarshipApplicationForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .models import PitchDeck, Dashboard, VendorApplication, Venue, Scholarship  
from social_django.models import UserSocialAuth
from django.contrib.auth import get_user_model
from django_eventstream import send_event


User = get_user_model()




######################################################################

def vendor_about(request):
    return render(request, 'belonging/vendor.html')
#########################################################################
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Assuming 'phone_number' is a field in your CustomUser model
            user.phone_number = form.cleaned_data['phone_number']
            user.save()
            login(request, user)
            return redirect('applicant_dashboar')  # Use the name of the URL pattern
    else:
        form = CustomUserCreationForm()
    return render(request, 'belonging/registration.html/', {'form': form})
#####################################################################################
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        username = request.POST['username']  # Changed from 'email' to 'username'
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('applicant_dashboard')
        else:
            # If the login is unsuccessful, re-render the page with the form and an error message
            return render(request, 'belonging/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = CustomAuthenticationForm()
        return render(request, 'belonging/login.html', {'form': form})
    #should make a route if their application has been approved, to route to 'default_dashboard'

##############################################################################
@login_required
def default_dashboard(request):
    dashboard_data = Dashboard.objects.all()
    return render(request, 'belonging/default_dashboard.html', {'dashboard_data': dashboard_data})

@login_required
def applicant_dashboard(request):
    user_pitch_decks = PitchDeck.objects.filter(user=request.user)
    scholarships = Scholarship.objects.all()  # Fetch scholarships
    vendor_applications = VendorApplication.objects.all()  # Fetch vendor applications

    # Prepare the context with all necessary data
    context = {
        'user_pitch_decks': user_pitch_decks,
        'scholarships': scholarships,
        'vendor_applications': vendor_applications,
        
    }
    scholarships = Scholarship.objects.all()  # Get all scholarship objects
    context = {'scholarships': scholarships}

    return render(request, 'belonging/applicant_dashboard.html', context)

@login_required
def scholarship_application(request):
    if request.method == 'POST':
        form = ScholarshipApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            send_event('applications', 'new_scholarship_application', {'id': application.id})

            # Prepare the email
            email = EmailMessage(
                subject='New Scholarship Application',
                body='A new scholarship application has been submitted.',
                to=['stephdelong93@gmail.com']
            )

            # Generate CSV data from the form
            csv_file_path = os.path.join(settings.MEDIA_ROOT, 'scholarship_applications.csv')
            with open(csv_file_path, 'a', newline='') as file:  # 'a' to append to the CSV
                writer = csv.writer(file)
                writer.writerow([
                    application.full_name,
                    application.date_of_birth,
                    application.age,
                    application.education_level,
                    application.gender,
                    application.business_description,
                    application.business_name,
                    application.video_link,
                    application.slide_deck.url if application.slide_deck else '',
                    application.pdf.url if application.pdf else ''
                ])

            # Attach the CSV file to the email
            email.attach_file(csv_file_path)
            email.send()

            # Redirect to the applicant dashboard
            return redirect('applicant_dashboard')
    else:
        form = ScholarshipApplicationForm()
    
    return render(request, 'belonging/scholarship_app.html', {'form': form})

@login_required
def vendor_application(request):
    
        form = VendorApplicationForm(request.POST, request.FILES)
        if request.method == 'POST' and form.is_valid():
            vendor_application = form.save(commit=False)
            vendor_application.user = request.user
            vendor_application.save()
            send_event('applications', 'new_vendor_application', {'id': vendor_application.id})

            # Prepare the email
            email = EmailMessage(
                subject='New Vendor Application',
                body='A new vendor application has been submitted.',
                to=['stephdelong93@gmail.com']
            )

            # Create a CSV file
            csv_file = os.path.join(settings.MEDIA_ROOT, 'vendor_applications.csv')
            with open(csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Username', 'Full Name', 'Date of Birth', 'Age', 'Education Level', 'Gender', 'Business Description', 'Business Name', 'Website Link', 'About Me', 'Logo URL', 'Business Proposal URL', 'Fee Structure URL'])
                writer.writerow([request.user.username, form.cleaned_data.get('full_name'), form.cleaned_data.get('date_of_birth'), form.cleaned_data.get('age'), form.cleaned_data.get('education_level'), form.cleaned_data.get('gender'), form.cleaned_data.get('business_description'), form.cleaned_data.get('business_name'), form.cleaned_data.get('website_link'), form.cleaned_data.get('about_me'), form.instance.logo.url if form.instance.logo else None, form.instance.business_proposal.url if form.instance.business_proposal else None, form.instance.fee_structure.url if form.instance.fee_structure else None])

            # Attach the CSV file to the email
            email.attach_file(csv_file)
            email.send()

            return redirect('applicant_dashboard')

        # If it's not a POST request, or the form is not valid, render the page with the form
        return render(request, 'belonging/vendor_app.html', {'form': form})



def donate_stripe(request):
    return render(request, 'belonging/donate.html')

def home_page(request):
    return render(request, 'belonging/index.html')

def about_view(request):
    return render(request, 'belonging/about.html')


def index_view(request):
    return render(request, 'belonging/index.html')

def involved_view(request):
    venues = Venue.objects.all()
    return render(request, 'belonging/involved.html', {'venues': venues})


def google_login(request):
    user = request.user
    try:
        user_social_auth = user.social_auth.get(provider='google-oauth2')
        # Handle authenticated user here
    except UserSocialAuth.DoesNotExist:
        # Handle unauthenticated user here
        return redirect('login')
    return redirect('belonging/default_dashboard')
