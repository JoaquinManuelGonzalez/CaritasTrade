from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from data_base.models import ExchangePost, ProductCategory
from view_profile.views import session_name


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
    category_id = id
    category = get_object_or_404(ProductCategory, id=category_id)
    if request.method == "POST":
        # Desactivar todas las publicaciones relacionadas con la categoría y establecer is_paused en True
        posts_to_pause = ExchangePost.objects.filter(product_category=category)
        for post in posts_to_pause:
            post.is_paused = True
            post.save()
        # Eliminar la categoría
        category.delete()
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
