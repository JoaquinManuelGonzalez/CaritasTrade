from django.shortcuts import render
from . import forms
from data_base.models import Workers


def edit_worker_profile(request, worker_id):
    user_session = request.session.get("id")
    user = Workers.objects.get(id=worker_id)
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
                        "Los datos del ayudante no han sido modificados. La Contraseña actual es incorrecta. Intente Nuevamente.",
                    )
                    return render(
                        request,
                        "edit_profile_worker_form.html",
                        {
                            "user": user,
                            "form": edit_form,
                            "session_id": user_session,
                            "user_session": False,
                            "birthday": format_birthday,
                        },
                    )
            user.save()
            return render(
                request, "edit_success_worker_message.html", {"id_user": user_session}
            )
        else:
            return render(
                request,
                "edit_profile_worker_form.html",
                {
                    "user": user,
                    "form": edit_form,
                    "session_id": user_session,
                    "user_session": False,
                    "birthday": format_birthday,
                },
            )
    else:
        edit_form = forms.edit_Form()
        return render(
            request,
            "edit_profile_worker_form.html",
            {
                "user": user,
                "form": edit_form,
                "session_id": user_session,
                "user_session": False,
                "birthday": format_birthday,
            },
        )
