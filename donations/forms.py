from django import forms
from data_base.models import Donation


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ["amount"]
        labels = {"amount": "Monto a donar"}
        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "min": "1",
                    "max": "1000000",
                    "step": "1",
                    "class": "form-control",
                }
            ),
        }
