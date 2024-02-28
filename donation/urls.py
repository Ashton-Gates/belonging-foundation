from django.urls import path
from . import views


app_name = 'donation'

urlpatterns = [
    path('payment/', views.donation_view, name='payment'),
    path('process_payment/<str:client_secret>/', views.process_payment, name='process_payment'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('change_password/', views.change_password, name='change_password'),
    path('donor_dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('donor_login/', views.donor_login, name='donor_login'),
    path('make_otp/', views.make_otp, name='make_otp'),
    path('process_payment/<str:client_secret>/', views.process_payment, name='process_payment'),

    ]
