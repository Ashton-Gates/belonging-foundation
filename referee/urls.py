# belonging-foundation/referee/urls.py

from django.urls import include, path
from . import views

app_name = 'referee'

urlpatterns = [
    path('referee_login/', views.login_view, name='login'),
    path('referee_register/', views.referee_register, name='register'),
    path('submit_referral/', views.submit_referral, name='submit_referral'),
    path('dashboard/', views.referee_dashboard, name='sponsor_dashboard'),
    path('sponsor_application/', views.sponsor_application, name='sponsor_application'),
    path('logout/', views.logout_view, name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('sponsor_form_submitted/', views.sponsor_form_submitted, name='sponsor_form_submitted'),
    path('onboard_form/', views.onboard_form, name='onboard_form'),


]
