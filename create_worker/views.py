from django.shortcuts import render
from . import forms
from data_base.models import Workers


def capitalize_element(data):
    data_list = data.split()
    data_list_capitalized = [data.lower().capitalize() for data in data_list]
    data_capitalized = " ".join(data_list_capitalized)
    return data_capitalized


def registration_form_worker(request):
    if request.method == "POST":
        registration_form = forms.Register_Form(request.POST)
        if registration_form.is_valid():
            dni = registration_form.cleaned_data["dni"]
            email = registration_form.cleaned_data["email"]
            name = registration_form.cleaned_data["name"]
            name_capitalized = capitalize_element(name)
            surname = registration_form.cleaned_data["surname"]
            surname_capitalized = capitalize_element(surname)
            phone_number = registration_form.cleaned_data["phone_number"]
            birth_day = registration_form.cleaned_data["birth_day"]
            password = registration_form.cleaned_data["password"]
            new_worker = Workers.objects.create(
                dni=dni,
                email=email,
                name=name_capitalized,
                surname=surname_capitalized,
                phone_number=phone_number,
                birth_day=birth_day,
                password=password,
            )
            return render(request, "success_worker_message.html")
        else:
            return render(
                request, "registration_worker_form.html", {
                    "session_id": request.session.get("id"),
                    "user_session": False,
                    "form": registration_form
                }
            )
    else:
        registration_form = forms.Register_Form()
        return render(
                request, "registration_worker_form.html", {
                    "session_id": request.session.get("id"),
                    "user_session": False,
                    "form": registration_form
                }
            )
