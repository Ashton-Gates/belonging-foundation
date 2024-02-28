#auction/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views import generic
from auction.models import Item
from .forms import CustomUserCreationForm

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def login_view(request):
    # Your login logic here
    return render(request, 'login.html')

def logout_view(request):
    # Your logout logic here
    return render(request, 'logout.html')

def dashboard_view(request):
    items = Item.objects.all()  # Fetch all auction items
    return render(request, 'dashboard.html', {'items': items})
