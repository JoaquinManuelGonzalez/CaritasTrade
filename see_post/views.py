import datetime
from django.shortcuts import get_object_or_404, redirect, render
from data_base.models import (
    ExchangePost,
    ExchangeSolicitude,
    Reputation,
    ProductCategory,
    Affiliate,
    Exchange,
)
from django.db.models import Avg
from view_profile.views import session_name


def see_post(request, id):
    if request.method == "GET" and request.session.get("id"):
        post = ExchangePost.objects.get(id=id)
        if post.is_active:
            if bool(post.image):
                post_image = post.image.decode("utf-8")
            else:
                post_image = None
            reputation = (
                Reputation.objects.filter(affiliate_id=post.affiliate_id)
                .aggregate(promedio=Avg("reputation"))
                .get("promedio")
            )
            category = ProductCategory.objects.filter(
                id=post.product_category_id
            ).first()
            return render(
                request,
                "see_post.html",
                {
                    "post": post,
                    "post_image": post_image,
                    "reputation": reputation,
                    "session_name": session_name(request),
                    "reputation_percentage": (reputation * 100) / 5,
                    "category": category,
                    "user_session": False,
                    "session_id": request.session.get("id"),
                    "role": request.session.get("role"),
                    "author_id": post.affiliate_id,
                    "author_name": Affiliate.objects.get(id=post.affiliate_id).name,
                    "own_post": post.affiliate_id == request.session.get("id"),
                    "posts": ExchangePost.objects.filter(
                        affiliate_id=request.session.get("id"),
                        is_active=True,
                        product_category=post.product_category,
                        is_finished=False,
                    ),
                },
            )
        else:
            return render(
                request,
                "see_post.html",
                {
                    "user_session": False,
                    "session_name": session_name(request),
                    "session_id": request.session.get("id"),
                },
            )
    else:
        return redirect("landing_page")


def send_exchange_solicitude(request, post_id_for):
    if (
        request.method == "POST"
        and request.session.get("id")
        and request.session.get("role") == "user"
    ):
        post_id = request.POST.get("post_id")
        previous_solicitude = ExchangeSolicitude.objects.filter(
            affiliate_id=request.session.get("id"),
            exchange_post_for_id=ExchangePost.objects.get(id=post_id_for),
        ).first()
        average_reputation = (
            Reputation.objects.filter(affiliate_id=request.session.get("id"))
            .aggregate(Avg("reputation"))
            .get("reputation__avg")
        )
        exchanges = Exchange.objects.filter(
            affiliate_1=request.session.get("id")
        ).count() + Exchange.objects.filter(
            affiliate_2=request.session.get("id")
        ).count()

        
        if average_reputation >= 3 and not bool(previous_solicitude) and exchanges < 5:
            ExchangeSolicitude.objects.create(
                affiliate_id=Affiliate.objects.get(id=request.session.get("id")),
                exchange_post_for_id=ExchangePost.objects.get(id=post_id_for),
                in_exchange_post_id=ExchangePost.objects.get(id=post_id),
                denied=False,
                timestamp=datetime.datetime.now(),
            )
            return render(
                request,
                "message.html",
                {
                    "message": "Solicitud de intercambio enviada con exito",
                    "type_of_alert": "success",
                },
            )
        message = ""
        if average_reputation < 3:
            message = "La reputacion actual es menor a 3 estrellas"
        elif bool(previous_solicitude):
            message = "Ya se envió una solicitud de intercambio para la publicación"
        else:
            message = "La cantidad de intercambios activos alcanzo el maximo"
        return render(
            request,
            "message.html",
            {
                "message": message,
                "type_of_alert": "danger",
            },
        )
