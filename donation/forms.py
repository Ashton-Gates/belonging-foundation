from django import forms
from .models import Donation, DonorAccount

class DonationForm(forms.Form):
    # Fields from DonorAccount model
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()  # This field is manually added, not part of the Donation model
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

    # Field from Donation model
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
