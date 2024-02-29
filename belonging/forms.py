from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Event
from accounts.models import CustomUser

from django.utils.translation import gettext_lazy as _  # Correct import

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    send_credentials = forms.BooleanField(required=False, label="Send Credentials")
    email_to_send = forms.EmailField(required=False, label="Email Address (optional)")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'company', 'user_type', 'send_credentials', 'email_to_send')


class CustomUserChangeForm(UserChangeForm):
    send_credentials = forms.BooleanField(required=False, label='Send credentials via email')
    email_to_send = forms.EmailField(required=False, label="Email Address (optional)")

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = '__all__'  # Adjust based on the fields you want to include



class CustomAuthenticationForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'input-field'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')


class EventForm(forms.ModelForm):
    class Meta:
        UserModel = Event
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
        fields = ['first_name', 'last_name']