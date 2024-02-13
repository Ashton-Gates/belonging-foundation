from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import ScholarshipApplication, Event, VendorApplication
from django.utils.translation import gettext_lazy as _  # Correct import

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Enter your email address.')
    phone_number = forms.CharField(required=True)


    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')  # Ensure email is saved.
        user.phone_number = self.cleaned_data.get('phone_number')
        user.is_customer = True
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')


class ScholarshipApplicationForm(forms.ModelForm):
    class Meta:
        model = ScholarshipApplication
        exclude = ('user', 'status', 'date_submitted', 'date_approved', 'date_rejected')
        fields = '__all__'


class EventForm(forms.ModelForm):
    class Meta:
        UserModel = Event
        fields = '__all__'

class VendorApplicationForm(forms.ModelForm):
    class Meta:
        model = VendorApplication
        fields = '__all__'
        exclude = ('user', 'status')



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
        fields = ['first_name', 'last_name']