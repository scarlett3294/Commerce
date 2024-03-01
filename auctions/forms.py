
from django import forms
from .models import Auction

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields =  fields = ['title', 'description', 'image', 'category', 'price', 'starting_bid', 'creator']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control'}),
        }

