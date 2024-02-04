from django.urls import path
from . import views
from .views import list_scholarship_applications, list_vendor_applications

urlpatterns = [
    path('review/', views.application_review, name='review_applications'),
    path('scholarship-applications/', list_scholarship_applications, name='list_scholarship_applications'),
    path('vendor-applications/', list_vendor_applications, name='list_vendor_applications'),
]
