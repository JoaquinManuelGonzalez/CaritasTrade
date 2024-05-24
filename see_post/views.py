from django.shortcuts import get_object_or_404, redirect, render
from data_base.models import ExchangePost, Reputation, ProductCategory, Affiliate
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
                    "posts": ExchangePost.objects.filter(affiliate_id= request.session.get("id"), is_active=True),
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


def get_posts_from_user(request, id):
    return render(
        request,
        "posts_as_options.html",
        {"posts": ExchangePost.objects.filter(affiliate_id=id)},
    )
