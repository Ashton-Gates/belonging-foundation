from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Event
from django.utils.translation import gettext_lazy as _  # Correct import

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Enter your email address.', widget=forms.EmailInput(attrs={'class': 'input-field'}))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'input-field'}))

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