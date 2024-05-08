from django import forms
from django.core.exceptions import ValidationError

class Register_Form(forms.Form):
    dni = forms.CharField(label="dni", max_length=8)
    email = forms.EmailField(label="email")
    name = forms.CharField(label="name", max_length=20)
    surname = forms.CharField(label="surname", max_length=20)
    phone_number = forms.CharField(label="phone_number", max_length=10)
    birth_day = forms.DateField(label="birth_day")
    password = forms.CharField(label="password", max_length=8)

    def clean_name(self):
        new_name = self.cleaned_data.get('name')
        if (len(new_name) > 20):
            raise ValidationError(
                "El/Los Nombre/s ingresado es inválido. Tamaño erróneo.")
        return new_name

    def clean_surname(self):
        new_surname = self.cleaned_data.get('surname')
        if (len(new_surname) > 20):
            raise ValidationError(
                "El/Los Apellido/s ingresado es inválido. Tamaño erróneo.")
        return new_surname

    def clean_phone_number(self):
        new_phone_number = self.cleaned_data.get('phone_number')
        if (len(new_phone_number) > 10):
            raise ValidationError(
                "El Número Telefónico ingresado es inválido. Tamaño erróneo.")
        return new_phone_number

    def clean_dni(self):
        new_dni = self.cleaned_data.get('dni')
        if (len(new_dni) != 8):
            raise ValidationError(
                "El D.N.I ingresado es inválido. Tamaño erróneo.")
        return new_dni