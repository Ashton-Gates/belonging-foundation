from django.urls import path
from . import views

urlpatterns = [
    path('', views.internal_login, name='internal_login'),
    path('scholarship-applications/', views.list_scholarship_applications, name='list_scholarship_applications'),
    path('vendor-applications/', views.list_vendor_applications, name='list_vendor_applications'),
    path('internal_registration/', views.internal_registration, name='internal_registration'),
    path('review_applications/', views.review_applications, name='review_applications'),  # Add this line
    path('get-latest-applications/', views.get_latest_applications, name='get_latest_applications'),


]