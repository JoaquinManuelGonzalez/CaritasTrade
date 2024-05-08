from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.core.exceptions import ValidationError
from datetime import date
import re

from . import forms
from data_base.models import Affiliate, Reputation


def check_email(new_email):
    if Affiliate.objects.filter(email=new_email).exists():
        raise ValidationError(
            "El email ingresado ya se encuentra registrado en el sistema.")


def check_dni(new_dni):
    if(Affiliate.objects.filter(dni=new_dni).exists()):
        raise ValidationError(
            "El D.N.I ingresado ya se encuentra registrado en el sistema.")


def check_birth_day(new_birth_day):
    minimum_age = date.today().year - 18
    if new_birth_day.year > minimum_age:
        raise ValidationError(
            "La fecha de nacimiento ingresada debe ser mayor a 18 años.")


def check_phone_number(new_phone_number):
    if (len(new_phone_number) > 10) or (not new_phone_number.startswith("221")):
        raise ValidationError(
            "El número telefónico ingresado es inválido. Debe ser un número telefónico proveniente de La Plata")


def check_password(new_password):
    if (len(new_password) < 8) or (not re.search(r"[a-zA-Z0-9\W_]", new_password)):
        raise ValidationError(
            "La contraseña ingresada es inválida. Debe contener 8 caracteres y contar con la combinación de números, letras y caracteres especiales.")


def registration_form(request):
    if request.method == "POST":
        registration_form = forms.Register_Form(request.POST)
        if registration_form.is_valid():
            try:
                registration_form.clean_dni()
                registration_form.clean_name()
                registration_form.clean_phone_number()
                registration_form.clean_surname()           
                dni = registration_form.cleaned_data["dni"]
                check_dni(dni)
                email = registration_form.cleaned_data["email"]
                check_email(email)
                birth_day = registration_form.cleaned_data["birth_day"]
                check_birth_day(birth_day)
                phone_number = registration_form.cleaned_data["phone_number"]
                check_phone_number(phone_number)
                password = registration_form.cleaned_data["password"]
                check_password(password)
            except ValidationError as e:
                registration_form.add_error(None, e)
                return render(request, "registration_form.html", {
                    "form": registration_form
                })
            new_reputation = Reputation.objects.create()
            new_affiliate = Affiliate.objects.create(
                dni=request.POST["dni"],
                email=request.POST["email"],
                name=request.POST["name"].lower().capitalize(),
                surname=request.POST["surname"].lower().capitalize(),
                phone_number=request.POST["phone_number"],
                birth_day=request.POST["birth_day"],
                password=request.POST["password"],
                reputation_id=new_reputation
            )
            return HttpResponseRedirect(reverse("landing_page"))
        else:
            return render(request, "registration_form.html", {
                "form" :registration_form
            })
    else:
        registration_form = forms.Register_Form()
        return render(request, "registration_form.html", {
            "form" :registration_form
        })
