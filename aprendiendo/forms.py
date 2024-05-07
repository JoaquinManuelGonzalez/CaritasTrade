from django import forms
from networkx import optimal_edit_paths

class createNewTask(forms.Form):
    dni = forms.CharField(label= "dni", max_length=8)
    email = forms.EmailField(label= "email")
    name = forms.CharField(label= "name",max_length=20)
    surname = forms.CharField(label= "surname",max_length=20)
    phone_number = forms.CharField(label= "phone_number",max_length=10)
    birth_day = forms.DateField(label='date', required=False)
    password = forms.CharField(label= "password",max_length=8, widget=forms.Textarea)
