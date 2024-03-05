#vendor/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth
from .forms import ItemForm

def onboard(request):
    return render(request, 'vendor/onboard.html')

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
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.vendor = request.user.vendor  # Assuming the user has a related Vendor instance
            item.save()
            return redirect('some_view_name')  # Redirect to a success page or dashboard
    else:
        form = ItemForm()
    return render(request, 'vendor/build_item.html', {'form': form})