from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

# Registration Form
class VenueRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[EmailValidator], widget=forms.EmailInput(attrs={'class': 'input-field'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-field'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'input-field'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'input-field'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# Login Form
class VenueLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-field'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field'}))
