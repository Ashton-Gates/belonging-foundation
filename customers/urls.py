#customers/urls.py

from django.urls import path
from .views import SignUpView, dashboard_view

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('dashboard/', dashboard_view, name='dashboard'),
    # Add other URLs for login, logout if not using Django's built-in views
]
