from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from . import forms
from data_base.models import Affiliate, Reputation


def registration_form(request):
    if request.method == "POST":
        registration_form = forms.Register_Form(request.POST)
        if registration_form.is_valid():
            dni = registration_form.cleaned_data['dni']
            email = registration_form.cleaned_data['email']
            name = registration_form.cleaned_data['name']
            surname = registration_form.cleaned_data['surname']
            phone_number = registration_form.cleaned_data['phone_number']
            birth_day = registration_form.cleaned_data['birth_day']
            password = registration_form.cleaned_data['password']
            new_reputation = Reputation.objects.create()
            new_affiliate = Affiliate.objects.create(
                dni=dni,
                email=email,
                name=name.lower().capitalize(),
                surname=surname.lower().capitalize(),
                phone_number=phone_number,
                birth_day=birth_day,
                password=password,
                reputation_id=new_reputation
            )
            return HttpResponseRedirect(reverse("log_in"))
        else:
            return render(request, "registration_form.html", {
                "form" :registration_form
            })
    else:
        registration_form = forms.Register_Form()
        return render(request, "registration_form.html", {
            "form" :registration_form
        })
