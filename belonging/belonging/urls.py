from django.contrib import admin
from django.urls import path
from .views import donate_stripe, register_view, login_view, dashboard_view, auction_dashboard, bidder_dashboard, donor_dashboard, recipient_dashboard, student_dashboard, vendor_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('registration/', register_view, name='registration'),
    path('default_dashboard/', dashboard_view, name='dashboard'),
    path('auction_dashboard/', auction_dashboard, name='auction_dashboard'),  # Fix the import here
    path('bidder_dashboard/', bidder_dashboard, name='dashboard'),
    path('donor_dashboard/', donor_dashboard, name='dashboard'),
    path('recipient_dashboard/', recipient_dashboard, name='dashboard'),
    path('student_dashboard/', student_dashboard, name='dashboard'),
    path('vendor_dashboard/', vendor_dashboard, name='dashboard'),
    path('donate/', donate_stripe, name='donate_stripe'),

]
