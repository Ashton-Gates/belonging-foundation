import random
import string
import stripe
from .forms import PaymentForm
from django.urls import reverse
from django.conf import settings
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import DonorAccount, Payment, OTPModel 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import get_user_model, authenticate, login

User = get_user_model()

def payment(request):
    form = PaymentForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        payment = form.save(commit=False)
        
        # Assign the user only if they are authenticated
        if request.user.is_authenticated:
            payment.user = request.user

        payment.save()

        # Create a Stripe PaymentIntent
        stripe.api_key = settings.STRIPE_PRIVATE_KEY
        intent = stripe.PaymentIntent.create(
            amount=int(payment.amount * 100),
            currency='usd',
            metadata={'payment_id': payment.id}
        )

        # Redirect to the payment processing view
        return redirect('donation:process_payment', client_secret=intent.client_secret)

    context = {'form': form}
    return render(request, 'payment.html', context)

def process_payment(request, client_secret):

    intent = None

    # Handle the successful payment

    if request.method == "POST":
        stripe.api_key = settings.STRIPE_PRIVATE_KEY
        
        try:

            intent = stripe.PaymentIntent.confirm(client_secret)

            if intent.status == 'succeeded':
                # Update the Payment model
                payment_id = intent.metadata['payment_id']
                payment = Payment.objects.get(id=payment_id)
                payment.paid = True
                payment.save()

                messages.success(request, 'Payment successful!')
                return redirect('success')
        
        except stripe.error.StripeError as e:
            # Handle exceptions from Stripe API
            messages.error(request, "Payment error: {}".format(e.user_message))
            # Optionally, redirect to a payment error page or show a message

    # This ensures 'intent' is checked for being None before attempting to access its attributes
    if intent is not None:
        return redirect(reverse('donation:payment', kwargs={'client_secret': intent.client_secret}))
    else:
        # Handle the case where intent couldn't be created or confirmed
        # Redirect to an appropriate page or show an error message
        messages.error(request, "There was an issue with your payment. Please try again.")
        return redirect('donation:payment')  # Adjust the redirect as necessary


def donation_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            with transaction.atomic():  # Use a transaction to ensure data integrity
                donor_account = None
                user = request.user

                # If the user is authenticated, get or create a DonorAccount for them
                if not isinstance(user, AnonymousUser):
                    donor_account, created = DonorAccount.objects.update_or_create(
                        user=user,
                        defaults={
                            'first_name': form.cleaned_data['first_name'],
                            'last_name': form.cleaned_data['last_name'],
                            'phone_number': form.cleaned_data['phone_number'],
                            'email': form.cleaned_data['email'],
                            'address': form.cleaned_data['address'],
                        }
                    )

                # Save payment information
                payment = form.save(commit=False)
                payment.user = donor_account  # Assign the donor_account to the payment
                payment.save()

                # Create a Stripe PaymentIntent
                stripe.api_key = settings.STRIPE_PRIVATE_KEY
                intent = stripe.PaymentIntent.create(
                    amount=int(payment.amount * 100),
                    currency='usd',
                    metadata={'payment_id': payment.id}
                )

                # Redirect to the payment processing view
                return redirect('donation:process_payment', intent.client_secret)
            # Handle form validation errors
        else:
            messages.error(request, "There was a problem with your submission.")
    else:
        form = PaymentForm()  # Make sure this is the form class you intend to use
    
    return render(request, 'donation/payment.html', {'form': form})

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

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def retrieve_stripe_info(request):
    email_or_transaction_id = request.GET.get('identifier', '')

    try:
        if "@" in email_or_transaction_id:  # rudimentary check to assume it's an email
            # List customers with the given email address
            customers = stripe.Customer.list(email=email_or_transaction_id).data
            if customers:
                customer_id = customers[0].id
                # Now retrieve charges or other information using this customer ID
                charges = stripe.Charge.list(customer=customer_id)
                # Process and return relevant information
                return JsonResponse({'charges': charges})
            else:
                return JsonResponse({'error': 'No customer found with that email.'})
        else:
            # Assume the identifier is a transaction ID and retrieve the charge
            charge = stripe.Charge.retrieve(email_or_transaction_id)
            # Process and return relevant information
            return JsonResponse({'charge': charge})
    except stripe.error.StripeError as e:
        # Handle the error
        body = e.json_body
        err  = body.get('error', {})
        return JsonResponse({'error': err.get('message')})

    # Generic error if identifier doesn't match any pattern
    return JsonResponse({'error': 'Invalid identifier provided.'})