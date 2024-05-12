from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
import random
import string
from data_base.models import Affiliate, Workers, AccountBlock
from . import forms
from caritasTrade.settings import DEFAULT_FROM_EMAIL as ADMIN_EMAIL


def raise_credentials_error():
    raise ValidationError(
        "No se ha podido iniciar sesión. El nombre de usuario o contraseña son inválidos."
    )

def raise_account_blocked_error(affiliate_username):
    raise ValidationError(
        f"No se ha podido iniciar sesión. La cuenta del usuario {affiliate_username} se encuentra bloqueada."
    )


def raise_new_account_block_error(affiliate_username):
    raise ValidationError(
        f"No se ha podido iniciar sesión. La cuenta del usuario {affiliate_username} ha sido bloqueada."
    )


def generate_otp(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    otp = "".join(random.choice(characters) for _ in range(length))
    return otp


def send_email(username, title, body):
    receiver = username
    subject = title
    message = body
    send_mail(subject, message, None, [receiver])


def block_affiliate_account(affiliate):
    new_account_block = AccountBlock.objects.create(
        affiliate_id=affiliate.id
    )
    subject = "Su Cuenta ha sido Bloqueada"
    message = f"Lamentamos informarle que la cuenta del usuario {affiliate.email} ha sido bloqueada temporalmente. Le notificaremos cuando este problema se solucione. Contactese a: comisionacional@caritas.org.ar para poder obtener más información."
    send_email(affiliate.email, subject, message)
    subject = "Nueva Cuenta Bloqueada"
    message = f"La Cuenta correspondiente al usuario {affiliate.email} ha sido bloqueada temporalmente. El sistema registrará el bloqueo y usted quedará a cargo de la resolución para la cuenta."
    send_email(ADMIN_EMAIL, subject, message)
    raise_new_account_block_error(affiliate.email)


def validate_Affiliate_password(affliate_password, password):
    if affliate_password != password:
        raise_credentials_error()
    

def validate_Worker_password(worker_password, password):
    if worker_password != password:
        raise_credentials_error()


def is_Admin(username):
    return username == ADMIN_EMAIL


def is_Worker(username, password, person_founded):
    try:
        worker = Workers.objects.get(email=username)
        person_founded = True
    except Workers.DoesNotExist:
        person_founded = False
    if person_founded:
        try:
            validate_Worker_password(worker.password, password)
        except ValidationError:
            raise_credentials_error()
        otp_code = generate_otp(8)
        subject = "Confirma tu Inicio de Sesión"
        message = f"El código OTP a ingresar para confirmar el Inicio de su Sesión es: {otp_code}"
        send_email(username, subject, message)
        return worker.id, person_founded, otp_code
    else:
        return None, None, False


def is_Affiliate(username, password):
    try:
        affiliate = Affiliate.objects.get(email=username)
    except Affiliate.DoesNotExist:
        raise_credentials_error()
    if (AccountBlock.objects.filter(affiliate_id=affiliate.id).exists()):
        raise_account_blocked_error(affiliate.email)
    try:
        validate_Affiliate_password(affiliate.password, password)
    except ValidationError:
        affiliate.login_attemps += 1
        affiliate.save()
        if affiliate.login_attemps == 3:
            block_affiliate_account(affiliate)
        raise_credentials_error()
    affiliate.login_attemps = 0
    affiliate.save()
    return affiliate.id


def login_view(request):
    if request.method == "POST":
        login_form = forms.Login_Form(request.POST)
        if login_form.is_valid():
            person_founded = False
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                worker_id, person_founded, otp_code = is_Worker(username, password, person_founded)
                if person_founded:
                    request.session['id'] = worker_id
                    if is_Admin(username):
                        request.session['role'] = "admin"
                    else:
                        request.session['role'] = "worker"
                    request.session['code'] = otp_code
                    return HttpResponseRedirect(reverse("confirm_session"))
                else:
                    affiliate_id = is_Affiliate(username, password)
                    request.session['id'] = affiliate_id
                    request.session['role'] = "user"
                    return HttpResponseRedirect(reverse("list_products"))
            except ValidationError as e:
                login_form.add_error(
                    None, e.message
                )
                return render(request, "log_in.html", {
                    "form" : login_form
                })
        else:
            return render(request, "log_in.html", {
                "form" : login_form
            })
    else:
        login_form = forms.Login_Form()
        return render(request, "log_in.html", {
            "form" : login_form
        })
    
def confirm_session_view(request):
    if request.method == "POST":
        confirm_session_form = forms.Confirm_Form(request.POST)
        if confirm_session_form.is_valid():
            input_code = confirm_session_form.cleaned_data['otp_code']
            if request.session['code'] != input_code:
                confirm_session_form.add_error(
                    None, "El código O.T.P ingresado no coincide con el código enviado. Intente nuevamente."
                )
                return render(request, "confirm_log_in.html", {
                    "form" : confirm_session_form
                })
            else:
                return HttpResponseRedirect(reverse("list_products"))
        else:
            return render(request, "confirm_log_in.html",{
                "form" : confirm_session_form
            })
    else:
        confirm_session_form = forms.Confirm_Form()
        return render(request, "confirm_log_in.html", {
                "form" : confirm_session_form
            })
