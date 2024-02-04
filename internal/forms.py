# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from belonging.models import CustomUser


class CustomLoginForm(AuthenticationForm):
    # You can add additional fields if needed
    remember_me = forms.BooleanField(required=False)


class InternalUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('is_internal_user',)

    def __init__(self, *args, **kwargs):
        super(InternalUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['is_internal_user'].initial = True
        self.fields['is_internal_user'].widget = forms.HiddenInput()