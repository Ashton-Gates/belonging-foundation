from django import forms
from .models import Payment, DonorAccount


class PaymentForm(forms.ModelForm):
    # Additional fields from DonorAccount model
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=15)
    email = forms.EmailField() 
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Payment
        fields = ('amount', 'description', 'first_name', 'last_name', 'phone_number', 'email', 'address')
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            # You can add more widgets for the new fields if needed
        }

    def save(self, commit=True):
        # Save the Payment instance
        payment = super().save(commit=False)

        # Process donor account information
        donor_account, created = DonorAccount.objects.update_or_create(
            email=self.cleaned_data.get('email'),
            defaults={
                'first_name': self.cleaned_data.get('first_name'),
                'last_name': self.cleaned_data.get('last_name'),
                'phone_number': self.cleaned_data.get('phone_number'),
                'address': self.cleaned_data.get('address'),
                # Ensure you set the user here if needed
            }
        )
        
        if commit:
            payment.user = donor_account.user  # Link the payment to the donor's account/user
            payment.save()
        return payment