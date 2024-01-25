from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import ScholarshipApplication, Event, VendorApplication




User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class CustomAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')


class ScholarshipApplicationForm(forms.ModelForm):
    class Meta:
        model = ScholarshipApplication
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'age', 
            'education_level', 'gender', 'business_name', 
            'business_description',
            # Add any other fields you wish to include from the model
        ]

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'time', 'time_zone', 'location', 'ticket_price', 'description', 'photo1', 'photo2', 'photo3', 'video']


class VendorApplicationForm(forms.ModelForm):
    class Meta:
        model = VendorApplication
        fields = ['logo', 'about_me', 'website_link', 'business_proposal', 'fee_structure', 'question1', 'question2', 'product_suite_overview', 'url_api_details', 'partnership_outcome']
