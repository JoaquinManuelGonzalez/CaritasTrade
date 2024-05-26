# forms.py
from django import forms
from data_base.models import Branches, Workers

class BranchForm(forms.Form):
    worker = forms.ModelChoiceField(queryset=Workers.objects.none(), label='Worker', widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    name = forms.CharField(max_length=20, label='Branch Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    latitude = forms.FloatField(label='Latitude', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    altitude = forms.FloatField(label='Altitude', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assigned_workers = Branches.objects.values_list('worker_id', flat=True)
        self.fields['worker'].queryset = Workers.objects.exclude(id__in=assigned_workers).exclude(email="caritas_trade_grupo38@outlook.com")

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        if Branches.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("El nombre de la Filial ya se encuentra registrado en el sistema.")
        return name

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get("latitude")
        altitude = cleaned_data.get("altitude")

        if Branches.objects.filter(latitude=latitude, altitude=altitude).exists():
            raise forms.ValidationError("Una Filial con esta Latitud y Altitud ya existe en el sistema.")

        return cleaned_data
    

class EditBranchForm(forms.Form):
    worker = forms.ModelChoiceField(queryset=Workers.objects.none(), label='Worker', widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    name = forms.CharField(max_length=20, label='Branch Name', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    latitude = forms.FloatField(label='Latitude', widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    altitude = forms.FloatField(label='Altitude', widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assigned_workers = Branches.objects.values_list('worker_id', flat=True)
        self.fields['worker'].queryset = Workers.objects.exclude(id__in=assigned_workers).exclude(email="caritas_trade_grupo38@outlook.com")

    def clean_name(self):
        name = self.cleaned_data['name'].lower()

        if not name:
            return name
        if Branches.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("El nombre de la Filial ya se encuentra registrado en el sistema.")
        
        return name

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get("latitude")
        altitude = cleaned_data.get("altitude")

        if not latitude or not altitude:
            return cleaned_data
        if Branches.objects.filter(latitude=latitude, altitude=altitude).exists():
            raise forms.ValidationError("Una Filial con esta Latitud y Altitud ya existe en el sistema.")

        return cleaned_data