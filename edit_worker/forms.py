from django import forms
from django.core.exceptions import ValidationError
from data_base.models import Affiliate,Workers
from datetime import date
import re

class edit_Form(forms.Form):
    email = forms.EmailField(label="Email", required=False)
    phone_number = forms.CharField(label="Número de teléfono", required=False)
    birth_day = forms.DateField(label="Fecha de nacimiento", required=False)
    password = forms.CharField(label="Contraseña", required=False)
    new_password = forms.CharField(label="Nueva Contraseña", required=False)
    confirm_new_password = forms.CharField(label="Confirmar Nueva Contraseña", required=False)

    def clean_phone_number(self):
        new_phone_number = self.cleaned_data.get('phone_number')
        if not new_phone_number:
            return new_phone_number
        if (len(new_phone_number) != 10):
            raise ValidationError(
                "Sus datos personales no han sido modificados. El Número Telefónico ingresado es inválido. Tamaño erróneo. Intente Nuevamente.")
        if (not re.match(r'^\d{10}$', new_phone_number)):
            raise ValidationError(
                "Sus datos personales no han sido modificados. El Número Telefónico ingresado debe estar conformado por números unicamente. Intente Nuevamente.")
        if not new_phone_number.startswith("221"):
            raise ValidationError(
                "Sus datos personales no han sido modificados. El número telefónico ingresado es inválido, debe ser un número telefónico proveniente de La Plata. Intente Nuevamente.")
        return new_phone_number


    def clean_email(self):
        new_email = self.cleaned_data.get('email')
        if not new_email:
            return new_email
        if (Affiliate.objects.filter(email=new_email).exists()) or (Workers.objects.filter(email=new_email).exists()):
            raise ValidationError(
                "Sus datos personales no han sido modificados. El email ingresado ya existe en el sistema. Intente Nuevamente.")
        return new_email

    def clean_birth_day(self):
        new_birth_day = self.cleaned_data.get('birth_day')
        if not new_birth_day:
            return new_birth_day
        
        minimum_age = date.today().year - 18
        if new_birth_day.year > minimum_age:
            raise ValidationError(
                "Sus datos personales no han sido modificados. La fecha de nacimiento ingresada debe ser mayor a 18 años. Intente Nuevamente.")
        return new_birth_day
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password
    
    
    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        password = self.cleaned_data.get('password')
        if not password:
            return password
        if not new_password:
            raise ValidationError(
                "Ingrese una nueva contraseña.")
        if (len(new_password) < 8) or (not re.search(r"[a-zA-Z]", new_password)) or (not re.search(r"\d", new_password)) or (not re.search(r"\W|_", new_password)):
            raise ValidationError(
                "Sus datos personales no han sido modificados. La Nueva Contraseña es errónea, debe cumplir con 8 caracteres como mínimo y contar con la combinación de números, letras y caracteres especiales. Intente Nuevamente.")
        return new_password
    
    
    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')
        
        if new_password != confirm_new_password:
            raise ValidationError("Sus datos personales no han sido modificados. La Confirmación para la Nueva Contraseña no coincide. Intente Nuevamente.")    
        return confirm_new_password


    