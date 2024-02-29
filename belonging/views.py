# views.py

from django.contrib.auth import get_user_model
from django.shortcuts import render


User = get_user_model()

def vendor_landing(request):
    return render(request, 'belonging/vendor_landing.html')

def scholar_landing(request):
    return render(request, 'belonging/scholar_landing.html')


def vendor_about(request):
    return render(request, 'belonging/vendor.html')

def donate_stripe(request):
    return render(request, 'belonging/donate.html')

def home_page(request):
    return render(request, 'belonging/index.html')

def about_view(request):
    return render(request, 'belonging/about.html')


def index_view(request):
    return render(request, 'belonging/index.html')

def involved_view(request):
    return render(request, 'belonging/involved.html')

