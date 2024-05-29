import base64
import datetime
from django.shortcuts import redirect, render
from data_base.models import ExchangePost, ProductCategory, Affiliate, ExchangeSolicitude
from .forms import ExchangeForm
from view_profile.views import session_name


# Create your views here.
def create_post(request):
    """
    Creates a new exchange post for an affiliate.

    If the user is not logged in, redirects to the landing page.

    If the user has already created 5 active posts, displays an error message.

    Otherwise, creates a new `ExchangePost` object with the form data and saves it to the database.
    The post is initially set to be inactive, and will be reviewed by the admin team.

    If the post is created successfully, a success message is displayed.
    """
    if not request.session.get("id"):
        return redirect("landing_page")

    form = ExchangeForm(request.POST or None, request.FILES or None)
    affiliate = Affiliate.objects.get(id=request.session.get("id"))
    num_posts = ExchangePost.objects.filter(
        affiliate_id=affiliate, is_rejected=False, is_active=True, is_paused=False
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
        form = ExchangeForm()
        success_message = "La publicación que creaste está ahora en estado pendiente. Nuestro equipo de trabajo la revisará y te notificará vía mail si fue aprobada o no."
    else:
        if not form.errors and num_posts >= 5:
            form.add_error(None, "Limite de publicaciones alcanzado")

    return render(
        request,
        "create_post.html",
        {
            "form": form,
            "categories": ProductCategory.objects.all(),
            "success_message": (
                success_message if form.is_valid() and num_posts < 5 else None
            ),
            "user_session": False,
            "session_id": request.session.get("id"),
            "session_name": session_name(request),
        },
    )
    