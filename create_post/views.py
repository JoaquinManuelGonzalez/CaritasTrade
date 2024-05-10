import base64
import datetime
from django.shortcuts import redirect, render
from data_base.models import ExchangePost, ProductCategory, Affiliate
from .forms import ExchangeForm


# Create your views here.
def create_post(request):
    if request.method == "GET" and request.session.get("id"):
        form = ExchangeForm()
        return render(
            request,
            "create_post.html",
            {
                "categories": ProductCategory.objects.all(),
                "form": form,
            },
        )
    elif request.method == "POST" and request.session.get("id"):
        form = ExchangeForm(request.POST, request.FILES)
        affiliate = Affiliate.objects.get(id=request.session.get("id"))
        num_posts = ExchangePost.objects.filter(
            affiliate_id=affiliate, is_rejected=False, is_active=False
        ).count()
        if form.is_valid() and num_posts < 5:
            post = ExchangePost(
                title=form.cleaned_data["title"],
                product_category_id=form.cleaned_data["category"].id,
                description=form.cleaned_data["description"],
                image=(
                    base64.b64encode(form.cleaned_data["image"].read())
                    if form.cleaned_data["image"]
                    else form.cleaned_data["image"]
                ),
                timestamp=datetime.datetime.now(),
                is_active=False,
                is_rejected=False,
                affiliate_id=request.session["id"],
            )
            post.save()
            return render(
                request,
                "create_post.html",
                {
                    "form": form,
                    "categories": ProductCategory.objects.all(),
                    "success_message": "La publicación que creaste está ahora en estado pendiente. Nuestro equipo de trabajo la revisará y te notificará vía mail si fue aprobada o no.",
                },
            )
        else:
            if not form.errors and num_posts >= 5:
                form.add_error(None, "Limite de publicaciones alcanzado")
            return render(
                request,
                "create_post.html",
                {
                    "form": form,
                    "categories": ProductCategory.objects.all(),
                },
            )
    else:
        return redirect("landing_page")
