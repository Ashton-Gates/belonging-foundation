from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import VenueLoginForm, VenueRegistrationForm
from django.contrib import messages

# Login View
def venue_login(request):
    if request.method == 'POST':
        form = VenueLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('venue/venue_home')  # Redirect to a success page.
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = VenueLoginForm()
    return render(request, 'venue/login.html', {'form': form})

# Registration View
def venue_register(request):
    if request.method == 'POST':
        form = VenueRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('venue/venue_home')  # Redirect to a success page.
    else:
        form = VenueRegistrationForm()
    return render(request, 'venue/register.html', {'form': form})

def venue_home(request):
    return render(request, 'venue_home.html')

def venue_profile(request):
    return render(request, 'venue_profile.html')

def venue_booking(request):
    return render(request, 'venue_booking.html')