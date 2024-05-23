from django.shortcuts import render
from . import forms
from data_base.models import Affiliate


def edit_profile(request):
    user_session = request.session.get("id")
    user = Affiliate.objects.get(id=user_session)
    fecha = user.birth_day
    format_birthday = fecha.strftime("%Y-%d-%m")

    if request.method == "POST":
        edit_form = forms.edit_Form(request.POST)
        if edit_form.is_valid():
            email = edit_form.cleaned_data["email"]
            phone_number = edit_form.cleaned_data["phone_number"]
            birth_day = edit_form.cleaned_data["birth_day"]
            password = edit_form.cleaned_data["password"]
            new_password = edit_form.cleaned_data["confirm_new_password"]
            # cambio los datos del usuario
            if email:
                user.email = email
            if phone_number:
                user.phone_number = phone_number
            if birth_day:
                user.birth_day = birth_day
            if password and new_password:
                if user.password == password:
                    user.password = new_password
                else:
                    edit_form.add_error(
                        None,
                        "Sus datos personales no han sido modificados. La Contraseña actual es incorrecta. Intente Nuevamente.",
                    )
                    return render(
                        request,
                        "edit_profile_form.html",
                        {
                            "user": user,
                            "form": edit_form,
                            "birthday": format_birthday,
                        },
                    )
            user.save()
            return render(
                request, "edit_success_message.html", {"id_user": user_session}
            )
        else:
            return render(
                request,
                "edit_profile_form.html",
                {
                    "user": user,
                    "form": edit_form,
                    "birthday": format_birthday,
                },
            )
    else:
        edit_form = forms.edit_Form()
        return render(
            request,
            "edit_profile_form.html",
            {
                "user": user,
                "form": edit_form,
                "birthday": format_birthday,
            },
        )
