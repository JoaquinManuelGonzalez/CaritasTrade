from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from data_base.models import ExchangePost, ExchangeSolicitude, ProductCategory
from view_profile.views import session_name
from log_in.views import send_email


def category_list(request):
    categories = ProductCategory.objects.all()
    return render(
        request,
        "category_list.html",
        {
            "categories": categories,
            "session_id": request.session.get("id"),
            "user_session": False,
            "session_name": session_name(request),
            "role": request.session.get("role"),
        },
    )


def category_add(request):
    if request.method == "POST":
        name = request.POST.get("name").lower().capitalize()
        if ProductCategory.objects.filter(name=name).exists():
            messages.error(request, f"La categoría {name} ya existe en el sistema")
        else:
            ProductCategory.objects.create(name=name)
            messages.success(request, "Categoría creada exitosamente")
            return redirect(reverse("category_list"))
    return render(
        request,
        "category_add.html",
        {
            "session_id": request.session.get("id"),
            "user_session": False,
        },
    )


def category_edit(request, id):
    category_id = id
    category = get_object_or_404(ProductCategory, id=category_id)
    if request.method == "POST":
        name = request.POST.get("name").lower().capitalize()
        if ProductCategory.objects.filter(name=name).exists():
            messages.error(request, f"La categoría {name} ya existe en el sistema")
        else:
            category.name = name
            category.save()
            messages.success(request, "Categoría modificada exitosamente")
            return redirect(reverse("category_list"))
    return render(
        request,
        "category_edit.html",
        {
            "category": category,
            "session_id": request.session.get("id"),
            "user_session": False,
            "session_name": session_name(request),
            "role": request.session.get("role"),
        },
    )


def category_delete(request, id):
    category = get_object_or_404(ProductCategory, id=id)
    if request.method == "POST":
        # Desactivar todas las publicaciones relacionadas con la categoría y establecer is_paused en True
        posts_to_pause = ExchangePost.objects.filter(product_category=category)
        send_email_paused_post = set()
        send_email_exchanges = set()
        
        if posts_to_pause:
            for post in posts_to_pause:
                post.is_paused = True
                post.save()

                # coleccion de emails dueños de posteos
                send_email_paused_post.add(post.affiliate.email)
                # coleccion de solicitudes de intercabios relacionados con el posteo
                solicitudes_to_pause = ExchangeSolicitude.objects.filter(exchange_post_for_id=post.id) |     ExchangeSolicitude.objects.filter(in_exchange_post_id=post.id)
            # Eliminar todas las solicitudes relacionadas con las publicaciones pausadas
            if solicitudes_to_pause:
                for solicitud in solicitudes_to_pause:
                    send_email_exchanges.add(solicitud.exchange_post_for_id.affiliate.email)
                    send_email_exchanges.add(solicitud.affiliate_id.email)
                    solicitud.delete()
        
        # Eliminar la categoría
        category.delete()
        
        # envio emails
        if send_email_paused_post:
            send_emails(list(send_email_paused_post), "owner_post")
        if send_email_exchanges:
            send_emails(list(send_email_exchanges), "solicitudes_post")
        messages.success(request, "Categoría eliminada exitosamente")
        return redirect(reverse("category_list"))
    return render(
        request,
        "category_delete.html",
        {
            "category": category,
            "session_id": request.session.get("id"),
            "user_session": False,
            "session_name": session_name(request),
            "role": request.session.get("role"),
        },
    )

def category_delete_all(request):
    if request.method == "POST":
        categories = ProductCategory.objects.all()
        for category in categories:
            posts_to_pause = ExchangePost.objects.filter(product_category=category)
            if posts_to_pause:
                for post in posts_to_pause:
                    post.is_paused = True
                    post.save()
                    solicitudes_to_pause = ExchangeSolicitude.objects.filter(exchange_post_for_id=post.id) | ExchangeSolicitude.objects.filter(in_exchange_post_id=post.id)
                    if solicitudes_to_pause:
                        for solicitud in solicitudes_to_pause:
                            solicitud.delete()
            category.delete()
        messages.success(request, "Todas las categorías han sido eliminadas exitosamente")
        return redirect(reverse("category_list"))
    return render(
        request,
        "category_delete_all.html",
        {
            "session_id": request.session.get("id"),
            "user_session": False,
            "session_name": session_name(request),
            "role": request.session.get("role"),
        },
    )

def send_emails(list, for_who):
    if for_who == "owner_post":
        title = "Su publicación fue pausada"
        body = """Buenos días,
        Le informamos que su publicación ha sido pausada debido a la eliminación de la categoría a la que pertenecía. Puede volver a publicarla en cualquier momento utilizando las categorías vigentes.

        Lamentamos las molestias ocasionadas."""
    else:
        title = "Su solicitud de intercambio fue eliminada"
        body = """Buenos días,
        Le informamos que su solicitud de intercambio ha sido eliminada debido a la eliminación de una categoría de productos a la cual pertenecía. Lamentamos los inconvenientes que esto pueda causarle.

        Le recordamos que puede volver a crear su publicación utilizando las categorías vigentes.

        Gracias por su comprensión."""

    if list:
        for username in list:
            send_email(username, title, body)
