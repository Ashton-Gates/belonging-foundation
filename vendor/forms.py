from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'starting_bid', 'image', 'condition', 'category']
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
        }
