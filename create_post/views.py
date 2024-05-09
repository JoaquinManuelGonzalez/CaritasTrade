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
    elif request.method == "POST" and request.sesssion.get("id"):
        form = ExchangeForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            post = ExchangePost(
                title=form.cleaned_data["title"],
                product_category_id=form.cleaned_data["category"],
                description=form.cleaned_data["description"],
                image=form.cleaned_data["image"].read(),
                timestamp=datetime.datetime.now(),
                is_active=False,
                is_rejected=False,
                affiliate_id=Affiliate.objects.get(id=request.session["id"]),
            )
            post.save()
        else:
            print(form.errors)
        return redirect("landing_page")
    else:
        return redirect("landing_page")
