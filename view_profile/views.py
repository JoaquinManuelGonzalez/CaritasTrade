import base64
from pyexpat.errors import messages
from tkinter import image_names
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from data_base.models import Affiliate, ExchangePost, Affiliate_Need_Product, Products

# Create your views here.


def profile(request, id):
    user = Affiliate.objects.get(id=id)
    post = ExchangePost.objects.filter(affiliate_id=id, is_active=True)
    # decodifico las imagenes
    decoded_images = []
    for p in post:
        if p.image:
            image_data = p.image.decode("utf-8")
            decoded_images.append(image_data)
        else:
            decoded_images.append(None)

    combined_data = list(zip(decoded_images, post))
    # armo la lista de deseos
    need_list = Affiliate_Need_Product.objects.filter(affiliate_id=id)
    products = []
    for need in need_list:
        product = Products.objects.get(
            id=need.id
        )  # Filtrar la tabla de productos por el ID
        products.append(product)  # Agregar el producto a la lista de productos

    session_id = request.session.get("id")
    user_session = session_id == id
    return render(
        request,
        "profile.html",
        {
            "session_id": session_id,
            "user_session": user_session,
            "user": user,
            "combined_data": combined_data,
            "need_products": products,
        },
    )


def confirm_sign_off(request):
    request.session["id"] = None
    return HttpResponseRedirect(reverse("landing_page"))
    # preguntar a fran como hacer que en la pantalla cuando se toque el cierre de sesion pida confirmacion y luego del mismo ejecute el sign_off.


def delete_post(request, id):
    if request.method == "POST" and request.session.get("id"):
        post_id = id
        post = ExchangePost.objects.get(id=post_id)
        creator = Affiliate.objects.get(id=post.affiliate_id)
        if creator.id == request.session.get("id"):
            post.delete()
            user = Affiliate.objects.get(id=request.session.get("id"))
            post = ExchangePost.objects.filter(
                affiliate_id=request.session.get("id"), is_active=True
            )
            # decodifico las imagenes
            decoded_images = []
            for p in post:
                if p.image:
                    image_data = p.image.decode("utf-8")
                    decoded_images.append(image_data)
                else:
                    decoded_images.append(None)
            combined_data = list(zip(decoded_images, post))
            # armo la lista de deseos
            need_list = Affiliate_Need_Product.objects.filter(affiliate_id=id)
            products = []
            for need in need_list:
                product = Products.objects.get(
                    id=need.id
                )  # Filtrar la tabla de productos por el ID
                products.append(product)  # Agregar el producto a la lista de productos

            session_id = request.session.get("id")
            user_session = True
            return render(
                request,
                "profile.html",
                {
                    "session_id": session_id,
                    "user_session": user_session,
                    "user": user,
                    "combined_data": combined_data,
                    "need_products": products,
                    "success_message": "La publicación se ha eliminado con éxito",
                },
            )
    else:
        return HttpResponseRedirect("landing_page")
