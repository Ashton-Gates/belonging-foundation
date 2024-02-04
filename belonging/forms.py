from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import ScholarshipApplication, Event, VendorApplication
from django.utils.translation import gettext_lazy as _  # Correct import

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Enter your email address.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)  # Add all required fields.

    # If you have custom fields that require validation, add them here.
    def clean_custom_field(self):
        # Perform custom validation for a field named 'custom_field'.
        custom_field = self.cleaned_data.get('custom_field')
        # Validation logic...
        return custom_field

class CustomAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')


class ScholarshipApplicationForm(forms.ModelForm):
    class Meta:
        model = ScholarshipApplication
        fields = '__all__'


class EventForm(forms.ModelForm):
    class Meta:
        UserModel = Event
        fields = '__all__'

class VendorApplicationForm(forms.ModelForm):
    class Meta:
        model = VendorApplication
        fields = '__all__'



class RegistrationFormStepOne(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class RegistrationFormStepTwo(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'user_type']