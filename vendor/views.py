from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth


def vendor_landing(request):
    return render(request, 'vendor/vendor_landing.html')

def vendor_login(request):
    return render(request, 'vendor/vendor_login.html')

def vendor_register(request):
    return render(request, 'vendor/vendor_registration.html')

def vendor_dashboard(request):
    return render(request, 'vendor/vendor_dashboard.html')

def vendor_app(request):
    return render(request, 'vendor/vendor_app.html')

def build_item(request):
    return render(request, 'vendor/build_item.html')

