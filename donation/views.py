from django.shortcuts import render, redirect
from .forms import DonationForm
from .models import DonorAccount
import stripe
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from .models import OTPModel 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Donation


User = get_user_model()

def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')

        # Assuming OTPModel has a field for the user, otp, and expiration time
        try:
            user = User.objects.get(email=email)
            otp_record = OTPModel.objects.get(user=user, otp=otp)

            # Check if OTP is expired
            if otp_record.is_expired():
                messages.error(request, 'OTP has expired. Please request a new one.')
                return redirect('request_otp')  # Replace with your actual URL name for requesting a new OTP

            # Log the user in
            login(request, user)

            # Redirect to change password page
            return redirect('change_password')

        except (User.DoesNotExist, OTPModel.DoesNotExist):
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('verify_otp')

    return render(request, 'donation/donor_login.html')


def donation_view(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            # Process donor account information
            donor_account, created = DonorAccount.objects.update_or_create(
                email=form.cleaned_data.get('email'),
                defaults={
                    'first_name': form.cleaned_data.get('first_name'),
                    'last_name': form.cleaned_data.get('last_name'),
                    'phone_number': form.cleaned_data.get('phone_number'),
                    'address': form.cleaned_data.get('address'),
                }
            )
            
            # Process donation information
            Donation.objects.create(
                donor=donor_account,
                amount=form.cleaned_data.get('amount'),
                # Add other fields as necessary
            )
            
            messages.success(request, "Thank you for your donation!")
            return redirect('https://pay.belonging.foundation/b/test_bIYaHGdWK5gz1K8aEE')
        else:
            messages.error(request, "There was a problem with your submission.")
    else:
        form = DonationForm()
    
    return render(request, 'donation/donate_form.html', {'form': form})
    
def process_payment(request, amount_cents):
    stripe.api_key = 'sk_test_51ObDcEKj0Am5FA1U8mu0YIyaYWgntAdOudVoidLPiCJlC9Ynm1WPHkIvrMFgy3Sph8JEOXARvuNDWoYEXNyFL1G30020D0t41u'
    token = request.POST['stripeToken']  # Token created by Stripe's Checkout or Elements

    try:
        charge = stripe.Charge.create(
            amount=amount_cents,
            currency='usd',
            description='Donation',
            source=token,
        )
        return charge.id
    except stripe.error.StripeError as e:
        # Handle the error
        return None
    
def donor_account_view(request):
    # Get the donor account for the current user
    donor_account = DonorAccount.objects.get(user=request.user)
    return render(request, 'donation/donor_account.html', {'donor_account': donor_account})


def donor_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('verify_otp')  # Assuming you have a separate OTP verification step
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'donation/donor_login.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user = request.user
        user.set_password(new_password)
        user.save()
        # Log the user back in after password change
        login(request, user)
        return redirect('donor_dashboard')
    return render(request, 'change_password.html')

@login_required
def donor_dashboard(request):
    return render(request, 'donation/donor_dashboard.html')


def make_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            # Check if the user has an associated DonorAccount
            user = User.objects.get(email=email)
            donor_account = DonorAccount.objects.get(user=user)
            
            # Generate a random 6-digit OTP
            otp = ''.join(random.choices(string.digits, k=6))
            
            # Create or update OTPModel instance for the user
            otp_model, created = OTPModel.objects.update_or_create(
                user=user, defaults={'otp': otp}
            )
            
            # Email the OTP to the user
            send_mail(
                'Your OTP',
                f'Your OTP is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'OTP has been sent to your email.')
            return redirect('donation:donor_login')  # Ensure this URL name matches your named URL for donor login
            
        except User.DoesNotExist:
            messages.error(request, 'No account found with the provided email.')
            return redirect('donation:make_otp')  # Ensure this URL name matches your named URL for OTP creation
        except DonorAccount.DoesNotExist:
            messages.error(request, 'You must donate before you can request an OTP.')
            return redirect('donation:make_otp')  # Same here for URL name
    else:
        return render(request, 'donation/make_otp.html')
