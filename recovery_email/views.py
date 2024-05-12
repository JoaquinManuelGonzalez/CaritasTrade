from django.shortcuts import render, redirect
from data_base.models import Affiliate
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import send_mail        
# Create your views here.

def see_users(request):
    users = Affiliate.objects.filter(accountblock__is_permanent=False)
    return render(request, "see_temporally_blocked_users.html", {"users": users})

def send_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        sender = 'tomeik125@gmail.com'
        receiver = email
        subject = 'Mail de recuperacion de cuenta'
        message = f'Buen dia, le proveo el link para que recuperar su cuenta: '
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

def recover_page(request):
    return render(request, "recover_page.html")

def recovered(request):
    return render(request, "recovered.html")

def recovery(request):
    
    return redirect("recovered")