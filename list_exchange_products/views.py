from django.shortcuts import render
from data_base.models import (
    Affiliate,
    ExchangePost,
    ProductCategory,
    Reputation,
)
from view_profile.views import session_name, decode_images


def list_products(request):
    role = request.session.get("role")
    post = ExchangePost.objects.filter(is_active=True, is_paused=False)

    query = request.GET.get("q")
    category = request.GET.get("category")
    response_rating = request.GET.get("rating")

    if query:
        post = post.filter(title__icontains=query)
    if category:
        post = post.filter(product_category_id=category)

    if response_rating:
        rating = float(response_rating)

        id_de_afiliados_con_mayor = Reputation.objects.filter(
            reputation__gt=rating
        ).values_list("affiliate", flat=True)
        afiliados_con_reputacion_mayor = Affiliate.objects.filter(
            id__in=id_de_afiliados_con_mayor
        )
        posteos_coincidentes = ExchangePost.objects.filter(
            affiliate_id__in=afiliados_con_reputacion_mayor,
            is_rejected=False,
            is_active=True,
        )
        post = post.filter(id__in=posteos_coincidentes.values_list("id", flat=True))
    # decodifico las imagenes
    combined_data = decode_images(post)
    categories = ProductCategory.objects.all()
    return render(
        request,
        "exchange_product_list.html",
        {
            "post": post,
            "session_id": request.session.get("id"),
            "user_session": False,
            "session_name": session_name(request),
            "combined_data": combined_data,
            "categories": categories,
            "role": role,
        },
    )
