from django.shortcuts import render, redirect
from data_base.models import ExchangePost, AccountBlock, Affiliate, Workers_AccountBlock, Workers
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

# Create your views here.

def see_waiting_posts(request):
    if (request.session.get("role") == "user"):
        return redirect("landing_page")
    blocked_affiliates = AccountBlock.objects.values_list('affiliate_id', flat=True)
    posts = ExchangePost.objects.filter(is_active=False, is_rejected=False).exclude(affiliate_id__in=blocked_affiliates)
    post_info = []
    for post in posts:
        aux = {"id": post.id, "title": post.title, "description": post.description, "category": post.product_category.name, "image": None, "attempts": post.affiliate.rejected_posts}
        if post.image:
            image_data = post.image.decode("utf-8")
            aux["image"] = image_data
        post_info.append(aux)
    return render(request, "see_waiting_posts.html", {"posts": post_info, "role": request.session.get("role")})

def send_accept_email(email):
    send_mail(
        'Publicacion aceptada',
        f'Buen dia, le informamos que su publicacion ha sido aceptada y publicada con exito',
        None,
        [email],
        fail_silently=False,
    )

def send_reject_email(email):
    send_mail(
        'Publicacion rechazada',
        f'Buen dia, le informamos que su publicacion ha sido rechazada y se han incrementando la cantidad de publicaciones indebidas por usted',
        None,
        [email],
        fail_silently=False,
    )

def send_temporal_block_email(email):
    send_mail(
        'Bloqueo temporal',
        f'Buen dia, le informamos que su cuenta ha sido bloqueada temporalmente por alcanzar el limite de publicaciones indebidas. Por favor contactese a {settings.DEFAULT_FROM_EMAIL}',
        None,
        [email],
        fail_silently=False,
    )

def send_admin_email(email):
    send_mail(
        'Bloqueo temporal',
        f'Buen dia, le informamos que la cuenta del usuario {email} ha sido bloqueada',
        None,
        [settings.DEFAULT_FROM_EMAIL],
        fail_silently=False,
    )   

def accept(request):
    if request.method == 'POST':
        post_id = request.POST.get("id")
        post = ExchangePost.objects.filter(id=post_id).first()
        post.is_active = True
        post.save()
        affiliate = post.affiliate
        send_accept_email(affiliate.email)
    return redirect("see_waiting_posts")

def reject(request):
    if request.method == 'POST':
        post_id = request.POST.get("id")
        post = ExchangePost.objects.filter(id=post_id).first()
        post.is_rejected = True
        post.save()
        affiliate = post.affiliate
        affiliate.rejected_posts = affiliate.rejected_posts + 1
        affiliate.save()
        if (affiliate.rejected_posts < 3):
            send_reject_email(affiliate.email)
        else:
            AccountBlock.objects.create(affiliate=affiliate, is_permanent=False).save()
            send_temporal_block_email(affiliate.email)
            send_admin_email(affiliate.email)
    return redirect("see_waiting_posts")

def block(request):
    if request.method == 'POST':
        post_id = request.POST.get("id")
        affiliate = ExchangePost.objects.filter(id=post_id).first().affiliate
        worker = Workers.objects.filter(id=request.session.get("id")).first()
        if (request.session.get("role") == "admin"):
            account_block = AccountBlock.objects.filter(affiliate=affiliate).first()
            if (account_block):
                account_block.is_permanent = True
                account_block.save()
                Workers_AccountBlock.objects.create(worker=worker, timestamp=timezone.now(), account_block=account_block)
            else:
                account_block= AccountBlock.objects.create(affiliate=affiliate, is_permanent=True)
                Workers_AccountBlock.objects.create(worker=worker, timestamp=timezone.now(), account_block=account_block)
        else:
            return render(request, "captcha.html", {"affiliate": affiliate})
    return redirect("see_waiting_posts")

def worker_block(request):
    if request.method == 'POST':
        affiliate_id = request.POST.get("id")
        affiliate = Affiliate.objects.filter(id=affiliate_id).first()
        account_block = AccountBlock.objects.filter(affiliate=affiliate).first()
        worker = Workers.objects.filter(id=request.session.get("id")).first()
        if (account_block):
            account_block.is_permanent = True
            account_block.save()
            Workers_AccountBlock.objects.create(worker=worker, timestamp=timezone.now(), account_block=account_block)
        else:
            account_block= AccountBlock.objects.create(affiliate=affiliate, is_permanent=True)
            Workers_AccountBlock.objects.create(worker=worker, timestamp=timezone.now(), account_block=account_block)
    return redirect("see_waiting_posts")
