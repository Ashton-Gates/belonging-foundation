
# utils.py

from django.core.mail import send_mail
from django.conf import settings
import random

def generate_otp():
    return random.randint(100000, 999999)  # This is just an example, use a secure method!

def send_otp_via_email(email, otp):
    send_mail(
        'Your OTP',
        f'Your OTP is: {otp}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )