from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.mail import send_mail
from data_base.models import (
    Affiliate,
    ExchangePost,
    Affiliate_Need_Product,
    Products,
    Workers,
    ExchangeSolicitude
)


def session_name(request):
    role = request.session.get("role")
    session_id = request.session.get("id")
    if role == "user":
        session_user = Affiliate.objects.get(id=session_id)
    else:
        session_user = Workers.objects.get(id=session_id)
    return session_user.name


def decode_images(post):
    decoded_images = []
    for p in post:
        if p.image:
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


# VER EL TEMA DE COMO WORKER VER UN AFILAIDOhacer session_id e user_session aca o dentro de los if? que paso en el caso en que sos un worker que quiere ver un user?  se puede?
def profile(request, id):
    session_id = request.session.get("id")
    user_session = session_id == id
    role = request.session.get("role")
    if role == "user":
        user = get_object_or_404(Affiliate, id=id)
        post = ExchangePost.objects.filter(affiliate_id=id, is_active=True, is_paused=False)
        # decodifico las imagenes
        combined_data = decode_images(post)
        # armo la lista de deseos
        need_list = craft_need_list(id)
        return render(
            request,
            "profile.html",
            {
                "session_id": session_id,
                "user_session": user_session,
                "user": user,
                "session_name": session_name(request),
                "combined_data": combined_data,
                "need_products": need_list,
            },
        )
    else:
        user = get_object_or_404(Workers, id=id)
        return render(
            request,
            "worker_profile.html",
            {
                "session_id": session_id,
                "user_session": user_session,
                "user": user,
                "session_name": session_name(request),
                "role": role,
            },
        )


def confirm_sign_off(request):
    request.session["id"] = None
    return HttpResponseRedirect(reverse("landing_page"))


def notify(post_id, post):
    solicitudes = ExchangeSolicitude.objects.filter(exchange_post_for_id=post_id, denied=False).all()
    solicitudes.update(denied=True)
    emails = []
    for solicitud in solicitudes:
        emails.append(solicitud.affiliate_id.email)
    if emails:
        send_mail(
            "Solicitud de intercambio rechazada",
            f"Buen dia, le avisamos que su solicitud de intercambio de {post.title} a sido rechazada",
            None,
            emails,
            fail_silently=False,
        )


def delete_post(request, id):
    if request.method == "POST" and request.session.get("id"):
        post_id = id
        post = ExchangePost.objects.get(id=post_id)
        creator = Affiliate.objects.get(id=post.affiliate_id)
        if creator.id == request.session.get("id"):
            notify(post_id, post)
            post.delete()
            user = Affiliate.objects.get(id=request.session.get("id"))
            post = ExchangePost.objects.filter(
                affiliate_id=request.session.get("id"), is_active=True,is_paused=False
            )
            # decodifico las imagenes
            combined_data = decode_images(post)
            # armo la lista de deseos
            need_list = craft_need_list(id)

            session_id = request.session.get("id")
            user_session = True
            return render(
                request,
                "profile.html",
                {
                    "session_id": session_id,
                    "user_session": user_session,
                    "user": user,
                    "session_name": session_name(request),
                    "combined_data": combined_data,
                    "need_products": need_list,
                    "success_message": "La publicación se ha eliminado con éxito",
                },
            )
    else:
        return HttpResponseRedirect("landing_page")
