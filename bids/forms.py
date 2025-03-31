from django import forms
from django.views.generic import CreateView

from bids.models import Auction, Bid


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = '__all__'
        exclude = ('user', 'auction', 'created_at')


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = '__all__'
        exclude = ('user',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
