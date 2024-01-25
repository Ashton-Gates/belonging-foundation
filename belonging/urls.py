from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import vendor_application_view,  scholarship_application_view, account_management, involved_view, index_view, scholarship_view, impact_view, about_view, home_page, donate_stripe, register_view, login_view, default_dashboard, auction_dashboard, bidder_dashboard, donor_dashboard, recipient_dashboard, student_dashboard, vendor_dashboard

urlpatterns = [
    path('', home_page, name='home_page'),
    path('index/', index_view, name='home_page'),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('registration/', register_view, name='registration'),
    path('default_dashboard/', default_dashboard, name='dashboard'),
    path('auction_dashboard/', auction_dashboard, name='auction_dashboard'),  # Fix the import here
    path('bidder_dashboard/', bidder_dashboard, name='bidder_dashboard'),
    path('donor_dashboard/', donor_dashboard, name='donor_dashboard'),
    path('recipient_dashboard/', recipient_dashboard, name='recipient_dashboard'),
    path('student_dashboard/', student_dashboard, name='student_dashboard'),
    path('vendor_dashboard/', vendor_dashboard, name='vendor_dashboard'),
    path('scholarship/',scholarship_view, name='scholarship' ),
    path('donate/', donate_stripe, name='donate_stripe'),
    path('about/', about_view, name='about'),
    path('impact/', impact_view, name='impact'),
    path('involved/', involved_view, name='involved'),
    path('account_management/', account_management, name='account_management'),
    path('scholarship_app/', scholarship_application_view, name='scholarship_application'),
    path('scholarship_app', views.scholarship_application_view, name='scholarship_application'),
    path('vendor_app/', vendor_application_view, name='vendor_app' ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)