from django import forms


class Login_Form(forms.Form):
    username = forms.CharField(label="Nombre de Usuario")
    password = forms.CharField(label="Contraseña")