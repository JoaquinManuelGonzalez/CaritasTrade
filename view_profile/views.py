from pyexpat.errors import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from data_base.models import Affiliate, ExchangePost, Affiliate_Product, Products

# Create your views here.


def profile(request, id):
    user = Affiliate.objects.get(id=id)
    post = ExchangePost.objects.filter(affiliate_id=id, is_active=True)
    need_list = Affiliate_Product.objects.filter(affiliate_id=id)
    products = (
        []
    )  # Inicializar una lista vacía para almacenar los productos asociados al afiliado
    for need in need_list:  # Iterar sobre la lista de necesidades
        product = Products.objects.get(
            id=need.product_id
        )  # Filtrar la tabla de productos por el ID
        products.append(product)  # Agregar el producto a la lista de productos
    user_session = True #False
    if request.session.get("id") == id:
        user_session = True
    return render(
        request,
        "profile.html",
        {
            "user_session": user_session,
            "user": user,
            "post": post,
            "need_products": products,
        },
    )


def confirm_sign_off(request):
    request.session['id'] = None
    return HttpResponseRedirect(reverse("landing_page"))
    # preguntar a fran como hacer que en la pantalla cuando se toque el cierre de sesion pida confirmacion y luego del mismo ejecute el sign_off.