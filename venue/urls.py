from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from .views import (
    venue_register, venue_login, venue_home, venue_profile,
    venue_booking)

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('accounts/', include('allauth.urls')),    
    #path('login/', login_view, name='login'),
    #path('logout/', logout_view, name='logout'),
    path('login/', venue_login, name='venue_login'),
    path('register/', venue_register, name='register'),
    path('venue_home/', venue_home, name='venue_home'),
    path('venue_profile/', venue_profile, name='venue_profile'),
    path('venue_booking/', venue_booking, name='venue_booking')

]

#<a href="{% url 'belonging:index' %}" class="mb-5 btn btn-primary">Home</a>  