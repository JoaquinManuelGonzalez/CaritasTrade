from django.shortcuts import render, redirect
from django.utils import timezone
from data_base.models import Affiliate, Tokens, AccountBlock
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText      
import secrets
import string
from datetime import timedelta
# Create your views here.

def generate_token(dni, length=16):
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(length))
    Tokens.objects.create(affiliate_id=Affiliate.objects.filter(dni=dni).first(), token=token, expiration_date=timezone.now() + timedelta(hours=24)).save()
    return token

def see_users(request):
    if (request.session.get("role") != "admin"):
        return redirect("landing_page")
    users = Affiliate.objects.filter(accountblock__is_permanent=False)
    return render(request, "see_temporally_blocked_users.html", {"users": users})

def send_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        sender = 'tomeik125@gmail.com'
        receiver = email
        token = generate_token(request.POST.get('dni'))
        subject = 'Mail de recuperacion de cuenta'
        message = f'Buen dia, le proveo el link para que recuperar su cuenta: http://127.0.0.1:8000/recovery_email/recover_page/{token}'
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        user_smtp = 'tomeik125@gmail.com'
        password_smtp = 'gedi sfpz swrh aluq'
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(user_smtp, password_smtp)
        server.send_message(msg)
        server.quit()
    return redirect('see_users')

def recover_page(request, token):
    return render(request, "recover_page.html", {"token": token})

def recovered(request):
    return render(request, "recovered.html")

def recovery(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        affiliate = Affiliate.objects.filter(tokens__token=token, tokens__expiration_date__gt=timezone.now()).first()
        if (affiliate):
            AccountBlock.objects.filter(affiliate_id=affiliate.id).delete()
            return redirect("recovered")
        else:
            return redirect("landing_page")