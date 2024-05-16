from django.shortcuts import render, redirect
from django.utils import timezone
from data_base.models import Affiliate, Tokens, AccountBlock
import secrets
import string
from datetime import timedelta
from django.core.mail import send_mail


def generate_token(dni, length=16):
    alphabet = string.ascii_letters + string.digits
    token = "".join(secrets.choice(alphabet) for _ in range(length))
    Tokens.objects.create(
        affiliate_id=Affiliate.objects.filter(dni=dni).first(),
        token=token,
        expiration_date=timezone.now() + timedelta(hours=24),
    ).save()
    return token


def see_users(request):
    if request.session.get("role") == "user":
        return redirect("landing_page")
    users = Affiliate.objects.filter(accountblock__is_permanent=False)
    return render(request, "see_temporally_blocked_users.html", {"users": users})


def send_email(request):
    if request.method == "POST":
        email = request.POST.get("email")
    token = generate_token(request.POST.get("dni"))
    send_mail(
        "Mail de recuperacion de cuenta",
        f"Buen dia, le proveo el link para que recuperar su cuenta: http://127.0.0.1:8000/recovery_email/recover_page/{token}",
        None,
        [email],
        fail_silently=False,
    )
    return redirect("see_users")


def recover_page(request, token):
    return render(request, "recover_page.html", {"token": token})


def recovered(request):
    return render(request, "recovered.html")


def recovery(request):
    if request.method == "POST":
        token = request.POST.get("token")
        affiliate = Affiliate.objects.filter(
            tokens__token=token, tokens__expiration_date__gt=timezone.now()
        ).first()
        if affiliate:
            affiliate.rejected_posts = 0
            affiliate.login_attemps = 0
            affiliate.save()
            AccountBlock.objects.filter(affiliate_id=affiliate.id).delete()
            return redirect("recovered")
        else:
            return redirect("landing_page")
