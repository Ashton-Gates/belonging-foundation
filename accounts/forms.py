from django import forms
from .models import CustomUser

class MyPasswordResetForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email', 'id': 'emailField'}))
