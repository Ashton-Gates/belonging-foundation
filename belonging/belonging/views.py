
import csv
import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.core.mail import EmailMessage
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .models import PitchDeck, Dashboard, Item, Vendor, ScholarshipApplication, VendorApplication  
from .forms import ScholarshipApplicationForm
from django.http import HttpResponseForbidden



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'belonging/registration.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return dashboard_redirect_view(request)

        else:
    # If the login is unsuccessful, re-render the page with the form and an error message
            return render(request, 'belonging/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = CustomAuthenticationForm()
        return render(request, 'belonging/login.html', {'form': form})

@login_required
def dashboard_redirect_view(request):
    if request.user.is_authenticated:
        user_type = request.user.user_type
        if user_type == 'student':
            return redirect('student_dashboard')
        elif user_type == 'donor':
            return redirect('donor_dashboard')
        elif user_type == 'recipient':
            return redirect('recipient_dashboard')
        elif user_type == 'hosts':
            return redirect('host_dashboard')
        elif user_type == 'bidders':
            return redirect('bidder_dashboard')
        elif user_type == 'vendors':
            return redirect('vendor_dashboard')
        # Add other conditions for different user types
    else:
        return redirect('default_dashboard')

@login_required
def default_dashboard(request):
    dashboard_data = Dashboard.objects.all()
    return render(request, 'belonging/default_dashboard.html', {'dashboard_data': dashboard_data})

@login_required
def auction_dashboard(request):
    items = Item.objects.all()
    return render(request, 'belonging/auction_dashboard.html', {'items': items})

@login_required
def bidder_dashboard(request):

    return render(request, 'belonging/bidder_dashboard.html')
@login_required
def donor_dashboard(request):

    return render(request, 'belonging/donor_dashboard.html')
@login_required
def recipient_dashboard(request):

    return render(request, 'belonging/recipient_dashboard.html')
@login_required

def student_dashboard(request):

    return render(request, 'belonging/applicant_dashboard.html')

def student_dashboard_view(request):
    user_pitch_decks = PitchDeck.objects.filter(user=request.user)
    scholarships = ScholarshipApplication.objects.all()
    vendor_applications = VendorApplication.objects.all()  # Fetch vendor applications

    # Add any additional context data as needed
    context = {
        'scholarships': scholarships,
        'vendor_applications': vendor_applications,
        # ... other context data ...
    }


    return render(request, 'belonging/applicant_dashboard.html', context, {'scholarships': scholarships})

@login_required
def scholarship_application_view(request):
    # Check if the user is a student
    if not request.user.user_type == 'student':
        return HttpResponseForbidden("You are not authorized to view this page.")

    if request.method == 'POST':
        # Initialize filenames as None
        video_filename = None
        slide_deck_filename = None
        pdf_filename = None
        
        # Process form data
        full_name = request.POST.get('first_name') + ' ' + request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        age = request.POST.get('age')
        education_level = request.POST.get('education_level')
        gender = request.POST.get('gender')
        business_description = request.POST.get('business_description')
        business_name = request.POST.get('business_name')

        # File uploads
        video = request.FILES.get('video')
        slide_deck = request.FILES.get('slide_deck')
        pdf = request.FILES.get('pdf')

        # Save files
        fs = FileSystemStorage()
        if video:
            video_filename = fs.save(video.name, video)
        if slide_deck:
            slide_deck_filename = fs.save(slide_deck.name, slide_deck)
        if pdf:
            pdf_filename = fs.save(pdf.name, pdf)

        # Prepare the email
        email = EmailMessage(
            subject='New Scholarship Application',
            body='A new scholarship application has been submitted.',
            to=['stephdelong93@gmail.com']
        )

        # Create a CSV file
        csv_file = os.path.join(settings.MEDIA_ROOT, 'scholarship_applications.csv')
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Full Name', 'Date of Birth', 'Age', 'Education Level', 'Gender', 'Business Description', 'Business Name', 'Video URL', 'Slide Deck URL', 'PDF URL'])
            writer.writerow([full_name, date_of_birth, age, education_level, gender, business_description, business_name, fs.url(video_filename), fs.url(slide_deck_filename), fs.url(pdf_filename)])

        # Attach the CSV file to the email
        email.attach_file(csv_file)

        # Send the email
        email.send()

        # Redirect to a success page or dashboard
        return redirect('applicant_dashboard/')
    else:
        # If it's a GET request, render the scholarship application form
        return render(request, 'belonging/scholarship_app.html')


@login_required
def vendor_application_view(request):
    # Check if the user is a student
    if not request.user.user_type == 'student':
        return HttpResponseForbidden("You are not authorized to view this page.")

    if request.method == 'POST':
        # Initialize filenames as None
        video_filename = None
        slide_deck_filename = None
        pdf_filename = None
        
        # Process form data
        full_name = request.POST.get('first_name') + ' ' + request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        age = request.POST.get('age')
        education_level = request.POST.get('education_level')
        gender = request.POST.get('gender')
        business_description = request.POST.get('business_description')
        business_name = request.POST.get('business_name')

                # New fields processing
        logo = request.FILES.get('logo')
        about_me = request.POST.get('about_me')
        website_link = request.POST.get('website_link')
        business_proposal = request.FILES.get('business_proposal')
        fee_structure = request.FILES.get('fee_structure')  # Optional

        # File uploads
        video = request.FILES.get('video')
        slide_deck = request.FILES.get('slide_deck')
        pdf = request.FILES.get('pdf')

        # Save files
        fs = FileSystemStorage()
        if logo:
            logo_filename = fs.save(logo.name, logo)
        if business_proposal:
            business_proposal_filename = fs.save(business_proposal.name, business_proposal)
        if fee_structure:
            fee_structure_filename = fs.save(fee_structure.name, fee_structure)

        # Prepare the email
        email = EmailMessage(
            subject='New Scholarship Application',
            body='A new scholarship application has been submitted.',
            to=['stephdelong93@gmail.com']
        )

        # Create a CSV file
        csv_file = os.path.join(settings.MEDIA_ROOT, 'scholarship_applications.csv')
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Full Name', 'Date of Birth', 'Age', 'Education Level', 'Gender', 'Business Description', 'Business Name', 'Video URL', 'Slide Deck URL', 'PDF URL'])
            writer.writerow([full_name, date_of_birth, age, education_level, gender, business_description, business_name, fs.url(video_filename), fs.url(slide_deck_filename), fs.url(pdf_filename)])

        # Attach the CSV file to the email
        email.attach_file(csv_file)

        # Send the email
        email.send()

        # Redirect to a success page or dashboard
        return redirect('applicant_dashboard/')
    else:
        # If it's a GET request, render the scholarship application form
        return render(request, 'belonging/vendor_app.html')





def donate_stripe(request):
    return render(request, 'belonging/donate.html')

def home_page(request):
    return render(request, 'belonging/index.html')

def about_view(request):
    return render(request, 'belonging/about.html')

def impact_view(request):
    return render(request, 'belonging/impact.html')

def scholarship_view(request):
    return render(request, 'belonging/scholarship.html')

def index_view(request):
    return render(request, 'belonging/index.html')

def involved_view(request):
    return render(request, 'belonging/involved.html')

@login_required
def vendor_dashboard(request):
    vendor = request.user.vendor
    items = Item.objects.filter(vendor=vendor)
    return render(request, 'vendor_dashboard.html', {'items': items})

@login_required
def add_item(request):
    if request.method == 'POST':
        # Handle the form submission
        name = request.POST.get('name')
        description = request.POST.get('description')
        start_bid = request.POST.get('start_bid')
        image = request.FILES.get('image')
        vendor = request.user.vendor
        Item.objects.create(name=name, description=description, start_bid=start_bid, image=image, vendor=vendor)
        return redirect('vendor_dashboard')
    return render(request, 'build_item.html')


@login_required
def account_management(request):
    if request.method == 'POST':
        # Process the form submission, e.g., updating user details
        pass
    else:
        # Display the form with user details
        pass
    return render(request, 'account_management.html')
