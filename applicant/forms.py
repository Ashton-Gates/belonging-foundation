#applicant/forms.py

from django import forms
from django.contrib.auth import get_user_model, authenticate
from .models import ScholarshipApplication, VendorApplication
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



User = get_user_model()

class ApplicantRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'applicant'  # Set the user type to 'applicant'
        if commit:
            user.save()
        return user
    
class ApplicantLoginForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None or (self.user_cache.user_type != 'applicant'):
                raise forms.ValidationError(
                    "Please enter correct credentials for an applicant account."
                )
        return self.cleaned_data
    

class VendorApplicationForm(forms.ModelForm):
    class Meta:
        model = VendorApplication
        fields = '__all__'
        exclude = ('user', 'status')

    def save(self, commit=True):
        vendor_application = super().save(commit=False)
        vendor_application.user = self.request.user
        if commit:
            vendor_application.save()
        return vendor_application

class ScholarshipApplicationForm(forms.ModelForm):
    class Meta:
        model = ScholarshipApplication
        exclude = ('user', 'status', 'date_submitted', 'date_approved', 'date_rejected')
        fields = '__all__'
