from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ValidationError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random
import string
from data_base.models import Affiliate, Workers
from . import forms


def generate_otp(length):
    characters = string.ascii_letters + string.digits
    otp = "".join(random.choice(characters) for _ in range(length))
    return otp

def send_email(username):
    otp_code = generate_otp(8)
    email = username
    sender = "adm.caritastrade@gmail.com"
    receiver = email
    subject = "Confirma tu Inicio de Sesión"
    message = f"El código a ingresar es: {otp_code}"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    user_smtp = "adm.caritastrade@gmail.com"
    password_smtp = "gedi sfpz swrh aluq"
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(message, "plain"))
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(user_smtp, password_smtp)
    server.send_message(msg)
    server.quit()
    return redirect("see_users")


def is_Worker(username):
    if (Workers.objects.filter(email=username).exists):
        send_email(username)


def login_view(request):
    if request.method == "POST":
        login_form = forms.Login_Form(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            is_Worker(username)
            return HttpResponseRedirect(reverse("list_exchange_products"))
        else:
            return render(request, "log_in.html", {
                "form" : login_form
            })
    else:
        login_form = forms.Login_Form()
        return render(request, "log_in.html", {
            "form" : login_form
        })