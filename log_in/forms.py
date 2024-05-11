from django import forms


class Login_Form(forms.Form):
    username = forms.CharField(label="Nombre de Usuario")
    password = forms.CharField(label="Contraseña")

class Confirm_Form(forms.Form):
    otp_code = forms.CharField(label="otp_code")

    def clean_otp_code(self):
        otp_code = self.cleaned_data['otp_code']
        if len(otp_code) != 8:
            raise forms.ValidationError(
                "Código O.T.P inválido. Tamaño erróneo"
            )
        return otp_code