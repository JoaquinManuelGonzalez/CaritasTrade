from django.shortcuts import render
from django.db.models import Avg
from view_profile.views import session_name, decode_images
from data_base.models import Affiliate_Need_Product, Affiliate, ExchangePost, Reputation, ProductCategory


def has_product_in_favorites(request, post_id):
    session_id = request.session.get("id")
    favorites = Affiliate_Need_Product.objects.filter(affiliate_id=session_id)
    exchange_posts = ExchangePost.objects.filter(id__in=favorites.values('product'))
    if post_id in exchange_posts.values_list('id', flat=True):
        return True
    return False


def list_favorites_products(request):
    session_id = request.session.get("id")
    user_session = session_id == id
    favorites = Affiliate_Need_Product.objects.filter(affiliate_id=session_id)
    exchange_posts = ExchangePost.objects.filter(id__in=favorites.values('product'))
    combined_data = decode_images(exchange_posts)

    return render(request, "favorites.html", {
        "session_id": session_id,
        "user_session": user_session,
        "session_name": session_name(request),
        "combined_data": combined_data
    })


def delete_from_favorites(request, post_id):
    session_id = request.session.get("id")
    Affiliate_Need_Product.objects.get(affiliate=Affiliate.objects.get(id=session_id), product=ExchangePost.objects.get(id=post_id)).delete()
    return list_favorites_products(request)
    

def add_to_favorites(request, post_id):
    session_id = request.session.get("id")
    user_session = session_id == id

    post = ExchangePost.objects.get(id=post_id)
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
        if Affiliate_Need_Product.objects.filter(affiliate=Affiliate.objects.get(id=session_id), product=ExchangePost.objects.get(id=post_id)).exists():
            Affiliate_Need_Product.objects.get(affiliate=Affiliate.objects.get(id=session_id), product=ExchangePost.objects.get(id=post_id)).delete()
            is_in_favorite = has_product_in_favorites(request, post.id)
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
                    "is_in_favorites": is_in_favorite,
                    "message": "Producto eliminado de la Lista de Favoritos.",
                }
            )
        else:
            new_product = Affiliate_Need_Product.objects.create(
                affiliate=Affiliate.objects.get(id=session_id),
                product=ExchangePost.objects.get(id=post_id)
            )
            is_in_favorite = has_product_in_favorites(request, post.id)
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
                    "is_in_favorites": is_in_favorite,
                    "message": "Producto añadido a la Lista de Favoritos.",
                }
            )
        
