from django import forms
from django.core.exceptions import ValidationError
from data_base.models import Affiliate, Workers
from datetime import date
import re

class Register_Form(forms.Form):
    dni = forms.CharField(label="D.N.I", error_messages = { 
                 'required' : "Por favor ingrese un D.N.I."
                 })
    email = forms.EmailField(label="Email", error_messages = { 
                 'required' : "Por favor ingrese un Email."
                 })
    name = forms.CharField(label="Nombre", error_messages = { 
                 'required' : "Por favor ingrese un Nombre."
                 })
    surname = forms.CharField(label="Apellido", error_messages = { 
                 'required' : "Por favor ingrese un Apellido."
                 })
    phone_number = forms.CharField(label="Número de teléfono", error_messages = { 
                 'required' : "Por favor ingrese in Número de Teléfono."
                 })
    birth_day = forms.DateField(label="Fecha de nacimiento", error_messages = { 
                 'required' : "Por favor ingrese una Fecha de Nacimiento."
                 })
    password = forms.CharField(label="Contraseña", error_messages = { 
                 'required' : "Por favor ingrese una Contraseña."
                 })

    def clean_name(self):
        new_name = self.cleaned_data.get('name')
        if (len(new_name) > 20):
            raise ValidationError(
                "El Nombre ingresado es inválido. Tamaño erróneo.")
        if not re.fullmatch(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', new_name):
            raise ValidationError(
                "El Nombre ingresado es inválido. Un Nombre no puede poseer números ni caracteres especiales.")
        return new_name

    def clean_surname(self):
        new_surname = self.cleaned_data.get('surname')
        if (len(new_surname) > 20):
            raise ValidationError(
                "El Apellido ingresado es inválido. Tamaño erróneo.")
        if not re.fullmatch(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', new_surname):
            raise ValidationError(
                "El Apellido ingresado es inválido. Un Apellido no puede poseer números ni caracteres especiales.")
        return new_surname

    def clean_phone_number(self):
        new_phone_number = self.cleaned_data.get('phone_number')
        if (len(new_phone_number) != 10):
            raise ValidationError(
                "El Número Telefónico ingresado es inválido. Tamaño erróneo.")
        if (not re.match(r'^\d{10}$', new_phone_number)):
            raise ValidationError(
                "El Número Telefónico ingresado debe estar conformado por números unicamente.")
        if not new_phone_number.startswith("221"):
            raise ValidationError(
                "El número telefónico ingresado es inválido. Debe ser un número telefónico proveniente de La Plata.")
        return new_phone_number

    def clean_dni(self):
        new_dni = self.cleaned_data.get('dni')
        if (len(new_dni) != 8):
            raise ValidationError(
                "El D.N.I ingresado es inválido. Tamaño erróneo.")
        if (not re.match(r'^\d{8}$', new_dni)):
            raise ValidationError(
                "El D.N.I ingresado debe estar conformado por números unicamente.")
        if(Affiliate.objects.filter(dni=new_dni).exists()):
            raise ValidationError(
                "El D.N.I ingresado ya se encuentra registrado en el sistema.")
        return new_dni

    def clean_email(self):
        new_email = self.cleaned_data.get('email')
        if (Affiliate.objects.filter(email=new_email).exists()) or (Workers.objects.filter(email=new_email).exists()):
            raise ValidationError(
                "El email ingresado ya se encuentra registrado en el sistema.")
        return new_email

    def clean_birth_day(self):
        new_birth_day = self.cleaned_data.get('birth_day')
        minimum_age = date.today().year - 18
        if new_birth_day.year > minimum_age:
            raise ValidationError(
                "La fecha de nacimiento ingresada debe corresponder a la de una persona de mínimo 18 años de edad.")
        return new_birth_day
    
    def clean_password(self):
        new_password = self.cleaned_data.get('password')
        if (len(new_password) < 8):
            raise ValidationError(
                "La Contraseña ingresada es inválida. Tamaño erróneo.")
        if (not re.search(r"[a-zA-Z]", new_password)) or (not re.search(r"\d", new_password)) or (not re.search(r"\W|_", new_password)):
            raise ValidationError(
                "La contraseña ingresada es inválida. Debe contener 8 caracteres como mínimo y contar con la combinación de números, letras y caracteres especiales.")
        return new_password
    