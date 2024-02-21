#vendor/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# Corrected from `urlspatterns` to `urlpatterns`
urlpatterns = [
    path('vendor_login/', views.vendor_login, name='login'),
    path('vendor_register/', views.vendor_register, name='register'),
    path('vendor_landing/', views.vendor_landing, name='landing'),
    path('vendor_dashboard/', views.vendor_dashboard, name='dashboard'),
    path('vendor_app/', views.vendor_app, name='vendor_app'),
    path('build_item/', views.build_item, name='build_item'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

