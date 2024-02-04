from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from .views import (vendor_application, scholarship_application, 
                     involved_view, index_view, 
                     about_view, home_page, 
                    donate_stripe, register_view, login_view, default_dashboard,  
                    applicant_dashboard, 
                    register_view, vendor_about)

urlpatterns = [
    path('', home_page, name='home_page'),
    path('index/', index_view, name='index_view'),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('registration/', register_view, name='registration'),
    path('default_dashboard/', default_dashboard, name='default_dashboard'),
    path('applicant_dashboard/', applicant_dashboard, name='applicant_dashboard'),
    path('donate/', donate_stripe, name='donate_stripe'),
    path('about/', about_view, name='about'),
    path('involved/', involved_view, name='involved'),
    path('scholarship_app/', scholarship_application, name='scholarship_application'),
    path('vendor_app/', vendor_application, name='vendor_app'),
    path('vendor/', vendor_about, name='vendor_about'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('internal/', include('internal.urls')),
    path('events/', include('django_eventstream.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
