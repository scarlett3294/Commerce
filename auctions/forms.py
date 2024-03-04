from django import forms
from .models import Auction

class AuctionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['starting_bid'].required = False  # Set starting_bid as not required in the form

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.price = instance.starting_bid  # Set price equal to starting_bid
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Auction
        fields = ['title', 'description', 'image', 'category', 'starting_bid', 'creator']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control'}),
        }
