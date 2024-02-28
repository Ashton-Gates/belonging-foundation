from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from .views import (involved_view, index_view, 
about_view, home_page, donate_stripe, vendor_about)



urlpatterns = [
    path('', home_page, name='home_page'),
    path('index/', index_view, name='index_view'),
    path('admin/', admin.site.urls),
    path('donate/', donate_stripe, name='donate_stripe'),
    path('about/', about_view, name='about'),
    path('involved/', involved_view, name='involved'),
    path('vendor/', vendor_about, name='vendor_about'),
    path('social-auth/', include('social_django.urls', namespace='social')),   
    path('events/', include('django_eventstream.urls')),
    path('applicant/', include('applicant.urls', 'applicant')),
    path('donation/', include('donation.urls', namespace='donation')),
    path('referee/', include(('referee.urls', 'referee'))),
    path('venue/', include(('venue.urls', 'venue'), namespace='venue')),
    path('vendor/', include(('vendor.urls', 'vendor'), namespace='vendor')),
    path('auction/', include(('auction.urls', 'auction'))),
    path('customers', include(('customers.urls', 'customers'))),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
