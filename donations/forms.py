from django import forms
from data_base.models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': '1', 'step': '1', 'class': 'form-control'}),
        }