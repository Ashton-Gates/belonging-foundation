#applicant/forms.py

from django import forms
from accounts.models import CustomUser
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from .models import ScholarshipApplication, VendorApplication
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm




User = get_user_model()

class ApplicantRegistrationForm(UserCreationForm):
    email = forms.EmailField(validators=[EmailValidator()], widget=forms.EmailInput(attrs={'class': 'input-field'}))
    username = forms.CharField(
        label="Full Name",
        validators=[RegexValidator(regex='^[a-zA-Z0-9]*$')],
        widget=forms.TextInput(attrs={'class': 'input-field'})  # Changed placeholder here
    )
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        exclude = ('user_type',)
        widgets = {

            'password1': forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Password', 'style': 'max-width: 300px;', 'pattern': '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,};'}),
            'password2': forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Password Confirmation', 'style': 'max-width: 300px;', 'pattern': '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,};'}),
        }
    def __init__(self, *args, **kwargs):
        super(ApplicantRegistrationForm, self).__init__(*args, **kwargs)
        # Set the help text for the password confirmation field to an empty string
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""
           
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'applicant'  # Set the user type to 'applicant'
        if commit:
            user.save()
        return user
    
class ApplicantLoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
    password1 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1']

    def __init__(self, *args, **kwargs):
        super(ApplicantLoginForm, self).__init__(*args, **kwargs)
        # Remove the username field, and replace it with email.
        del self.fields['username']

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
    
    def clean(self):
        cleaned_data = super().clean()  # Call the parent class's clean method first
        
        # Check if all required fields are filled
        for field in self.fields:
            if self.fields[field].required and not cleaned_data.get(field):
                self.add_error(field, 'This field is required.')

        # Validate URL fields specifically
        url_validator = URLValidator()
        video_link = cleaned_data.get('video_link')
        if video_link:
            try:
                url_validator(video_link)
            except ValidationError:
                self.add_error('video_link', 'Enter a valid URL.')
        
        # You can add more custom validations as needed

        # Always return the full collection of cleaned data
        return cleaned_data
