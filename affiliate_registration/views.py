from django.shortcuts import render
from . import forms
from data_base.models import Affiliate, Reputation

def capitalize_element(data):
    data_list = data.split()
    data_list_capitalized = [data.lower().capitalize() for data in data_list]
    data_capitalized = ' '.join(data_list_capitalized)
    return data_capitalized

def registration_form(request):
    if request.method == "POST":
        registration_form = forms.Register_Form(request.POST)
        if registration_form.is_valid():
            dni = registration_form.cleaned_data['dni']
            email = registration_form.cleaned_data['email']
            name = registration_form.cleaned_data['name']
            name_capitalized = capitalize_element(name)
            surname = registration_form.cleaned_data['surname']
            surname_capitalized = capitalize_element(surname)
            phone_number = registration_form.cleaned_data['phone_number']
            birth_day = registration_form.cleaned_data['birth_day']
            password = registration_form.cleaned_data['password']
            new_reputation = Reputation.objects.create()
            new_affiliate = Affiliate.objects.create(
                dni=dni,
                email=email,
                name=name_capitalized,
                surname=surname_capitalized,
                phone_number=phone_number,
                birth_day=birth_day,
                password=password,
                reputation_id=new_reputation
            )
            return render(request, "success_message.html")
        else:
            return render(request, "registration_form.html", {
                "form" :registration_form
            })
    else:
        registration_form = forms.Register_Form()
        return render(request, "registration_form.html", {
            "form" :registration_form
        })
