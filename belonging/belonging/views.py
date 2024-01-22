from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Dashboard, Item, Vendor



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
            return redirect('belonging/default_dashboard')
        else:
            # Return an 'invalid login' error message.
            pass
    else:
        form = CustomAuthenticationForm()
    return render(request, 'default_dashboard.html', {'form': form})

def dashboard_redirect_view(request):
    if request.user.is_authenticated:
        user_type = request.user.user_type
        if user_type == 'student':
            return redirect('belonging/student_dashboard')
        elif user_type == 'donor':
            return redirect('belonging/donor_dashboard')
        elif user_type == 'recipient':
            return redirect('belonging/recipient_dashboard')
        elif user_type == 'hosts':
            return redirect('belonging/host_dashboard')
        elif user_type == 'bidders':
            return redirect('belonging/bidder_dashboard')
        elif user_type == 'vendors':
            return redirect('belonging/vendor_dashboard')
        # Add other conditions for different user types
    else:
        return redirect('belonging/default_dashboard')


def dashboard_view(request):
    dashboard_data = Dashboard.objects.all()
    return render(request, 'belonging/default_dashboard.html', {'dashboard_data': dashboard_data})


def auction_dashboard(request):
    items = Item.objects.all()
    return render(request, 'belonging/auction_dashboard.html', {'items': items})


def bidder_dashboard(request):

    return render(request, 'belonging/bidder_dashboard.html')

def donor_dashboard(request):

    return render(request, 'belonging/donor_dashboard.html')

def recipient_dashboard(request):

    return render(request, 'belonging/recipient_dashboard.html')

def student_dashboard(request):

    return render(request, 'belonging/student_dashboard.html')

def donate_stripe(request):
    return render(request, 'belonging/donate.html')



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
