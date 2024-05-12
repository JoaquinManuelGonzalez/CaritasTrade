from pyexpat.errors import messages
from tkinter import image_names
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from data_base.models import Affiliate, ExchangePost, Affiliate_Need_Product, Products, Workers


def decode_images(post):
    decoded_images = []
    for p in post:
        if p.image:
            image_data = p.image.decode("utf-8")
            image_data = p.image.decode("utf-8")
            decoded_images.append(image_data)
        else:
            decoded_images.append(None)
    combined_data = list(zip(decoded_images, post))
    return combined_data

def craft_need_list(id):
    need_list = Affiliate_Need_Product.objects.filter(affiliate_id=id)
    products = []
    for need in need_list:
        product = Products.objects.get(
            id=need.id
        )  # Filtrar la tabla de productos por el ID
    products = []
    for need in need_list:
        product = Products.objects.get(
            id=need.id
        )  # Filtrar la tabla de productos por el ID
        products.append(product)  # Agregar el producto a la lista de productos
    return products


#VER EL TEMA DE COMO WORKER VER UN AFILAIDOhacer session_id e user_session aca o dentro de los if? que paso en el caso en que sos un worker que quiere ver un user?  se puede?       
def profile(request, id):   
    session_id = request.session.get("id")
    user_session = session_id == id
    role = request.session.get("role")
    if role == 'user':
        user = Affiliate.objects.get(id=id)
        post = ExchangePost.objects.filter(affiliate_id=id, is_active=True)
        # decodifico las imagenes
        combined_data= decode_images(post)
        # armo la lista de deseos
        need_list = craft_need_list(id)

        return render(
            request,
            "profile.html",
            {
                "session_id": session_id,
                "user_session": user_session,
                "user": user,
                "combined_data": combined_data,
                "need_products": need_list,
            },
        )
    else:
        user = Workers.objects.get(id=id)
        
        return render( request,"worker_profile.html",
            {
                "session_id": session_id,
                "user_session": user_session,
                "user": user,
                "role":role
            },
        )


def confirm_sign_off(request):
    request.session["id"] = None
    request.session["id"] = None
    return HttpResponseRedirect(reverse("landing_page"))
    