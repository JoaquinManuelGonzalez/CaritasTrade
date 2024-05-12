from django.shortcuts import redirect, render
from data_base.models import ExchangePost, Reputation, ProductCategory
from django.db.models import Avg


# Create your views here.
def see_post(request, id):
    if request.method == "GET" and request.session.get("id"):
        post = ExchangePost.objects.get(id=id)
        if post.is_active:
            post_image = post.image.decode("utf-8")
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
                    "reputation_percentage": (reputation * 100) / 5,
                    "category": category,
                    "user_session": False,
                    "session_id": request.session.get("id"),
                },
            )
        else:
            return render(
                request,
                "see_post.html",
                {"user_session": False,
                 "session_id": request.session.get("id")},
            )
    else:
        return redirect("landing_page")
