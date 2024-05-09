from django import forms
from django.core.exceptions import ValidationError
from data_base.models import Affiliate, Workers


class Login_Form(forms.Form):
    username = forms.CharField(label="Nombre de Usuario")
    password = forms.CharField(label="Contraseña")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        ADMIN_EMAIL = "adm.caritastrade@gmail.com"
        if (Workers.objects.filter(ADMIN_EMAIL=username).exists):
            raise ValidationError(
                "Soy el admin"
            )
        