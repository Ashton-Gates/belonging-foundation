#applicant/urls.py


from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import (vendor_application, scholarship_application, login_view, applicant_dashboard,                    
download_vendor_pdf, download_scholarship_pdf, logout_view,
withdraw_application, validate_referee_id, delete_account, registration,
scholar_landing, vendor_landing)

app_name = 'applicant'


urlpatterns = [
    path('scholar_landing/', scholar_landing, name='scholar_landing'),
    path('vendor_landing/', vendor_landing, name = 'vendor_landing'),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', registration, name='registration'),
    path('applicant_dashboard/', applicant_dashboard, name='applicant_dashboard'),
    path('scholarship_app/', scholarship_application, name='scholarship_application'),
    path('vendor_app/', vendor_application, name='vendor_application'),
    path('scholarship_application/<int:application_id>/download/', download_scholarship_pdf, name='download_scholarship_pdf'),
    path('vendor_application/<int:application_id>/download/', download_vendor_pdf, name='download_vendor_pdf'),
    path('applications/<int:application_id>/withdraw/', withdraw_application, name='withdraw_application'),
    path('validate_referee_id/', validate_referee_id, name='validate_referee_id'),
    path('delete_account/', delete_account, name='delete_account'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
