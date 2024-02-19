# belonging-foundation/referee/views.py


import uuid
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import RefereeRegistrationForm, ReferralForm, SponsorApplicationForm, LoginForm
from .models import Referee, Scholarship
User = get_user_model()


# Create your views here.
def sponsor_about(request):
    return render(request, 'referee/sponsor_about.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('referee:sponsor_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            # Debugging help
            print(form.errors)
    else:
        form = LoginForm()
    return render(request, 'referee/referee_login.html', {'form': form})


def generate_unique_referee_id():
    return str(uuid.uuid4())[:10]

def referee_register(request):
    # Initialize form variable before the if statement to ensure it's always defined
    form = RefereeRegistrationForm(request.POST or None)  # This handles both GET and POST requests
    User = get_user_model()  # Correctly retrieves the custom user model

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            if User.objects.filter(username=username).exists():
                messages.error(request, "A user with that username already exists.")
                return redirect('referee:register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "A user with that email already exists.")
                return redirect('referee:register')
            else:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data.get('password'))
                user.save()
                unique_referee_id = generate_unique_referee_id()
                Referee.objects.create(user=user, referee_id=unique_referee_id)
                messages.success(request, "Registration successful. Please complete your onboarding form.")
                return redirect('referee:onboard_form')  # Make sure this URL name is correctly defined in your urls.py

    # Removed the erroneous print statement; form is now always defined
    return render(request, 'referee/referee_register.html', {'form': form})

@login_required
def submit_referral(request):
    if request.method == 'POST':
        form = ReferralForm(request.POST)
        if form.is_valid():
            referral = form.save(commit=False)
            referral.referee = request.user.referee_profile
            referral.save()
            form.send_email()  # Send the email
            messages.success(request, 'Referral submitted successfully.')
            return redirect('referee:sponsor_dashboard')
    else:
        form = ReferralForm()
    return render(request, 'referee/submit_referral.html', {'form': form})


@login_required
def referee_dashboard(request):
    scholarships = Scholarship.objects.all()
    return render(request, 'referee/dashboard.html', {'scholarships': scholarships})


def sponsor_application(request):
    if request.method == 'POST':
        form = SponsorApplicationForm(request.POST)
        if form.is_valid():
            sponsor_application = form.save(commit=False)
            sponsor_application.user = request.user
            sponsor_application.save()
            # Assuming you create Referee instance upon sponsor application approval
            # Referee.objects.create(user=request.user, referee_id="UniqueRefereeID")
            return redirect('some_success_view')
    else:
        form = SponsorApplicationForm()

    return render(request, 'belonging/onboard_form.html', {'form': form})

def logout_view(request):
    logout(request)
    # Redirect to a success page, such as the home page
    return redirect('referee:login')


@login_required
def delete_account(request):
    if request.method == 'POST':
        # Delete the user's account
        request.user.delete()
        logout(request)
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home')  # Redirect to the homepage or a goodbye page
    else:
        # If it's not a POST request, just show the confirmation page
        return render(request, 'referee/delete_account.html')


@login_required
def onboard_form(request):
    if request.method == 'POST':
        form = SponsorApplicationForm(request.POST)
        if form.is_valid():
            sponsor_application = form.save(commit=False)
            sponsor_application.user = request.user  # Assuming a ForeignKey to User
            sponsor_application.save()
            messages.success(request, 'Your application has been submitted for review.')
            return redirect('referee:dashboard')  # Adjust as necessary
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SponsorApplicationForm()
    return render(request, 'referee/onboard_form.html', {'form': form})

@login_required
def sponsor_form_submitted(request):
    return render(request, 'referee/sponsor_form_submitted.html')


@login_required
def sponsor_dashboard(request):
    return render(request, 'referee/sponsor_dashboard.html')