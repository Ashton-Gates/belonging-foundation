from django import forms
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from referee.models import Referral
from .models import Scholarship, SponsorApplication
from django.contrib.auth import authenticate



User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Invalid username or password.')
            if not user.is_active:
                raise forms.ValidationError('This account is inactive.')
        return self.cleaned_data

class DenialFeedbackForm(forms.Form):
    feedback = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), label="Feedback for Denial")

class SponsorApplicationForm(forms.ModelForm):
    class Meta:
        model = SponsorApplication
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'gender', 'why_sponsor', 'qualifications']

class RefereeRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ReferralForm(forms.ModelForm):
    class Meta:
        model = Referral
        fields = ['nominee_name', 'nominee_email', 'nominee_phone_number', 'scholarship', 'justification']
        widgets = {
            'justification': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(ReferralForm, self).__init__(*args, **kwargs)
        self.fields['scholarship'].queryset = Scholarship.objects.all()

    def send_email(self):
        # Send an email to the nominee
        send_mail(
            'You have been nominated for a scholarship',
            'Message content.',
            'from@example.com',
            [self.cleaned_data['nominee_email']],
            fail_silently=False,
        )