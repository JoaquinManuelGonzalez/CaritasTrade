from django.http import HttpResponse
from django.shortcuts import redirect, render
from requests import session
from list_exchange_products.views import session_name
from data_base.models import Branches, EcommercePost, ExchangePost, ProductCategory


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


# Create your views here.
def list_ecommerce(request):
    posts = EcommercePost.objects.filter(stock__gt=0)

    query = request.GET.get("q")
    category = request.GET.get("category")

    if query:
        posts = posts.filter(title__icontains=query)
    if category:
        posts = posts.filter(product_category_id=category)
    if not request.session.get("id"):
        return redirect("landing_page")
    print(decode_images(posts))
    return render(
        request,
        "ecommerce.html",
        {
            "posts": decode_images(posts),
            "session_id": request.session.get("id"),
            "role": request.session.get("role"),
            "user_session": False,
            "session_name": session_name(request),
            "categories": ProductCategory.objects.all(),
        },
    )


def see_ecommerce_post(request, id):
    post = EcommercePost.objects.get(id=id)
    post_image = None
    if bool(post.image):
        post_image = post.image.decode("utf-8")
    own_post = False
    print(request.session.get("role") == "worker")
    print(Branches.objects.filter(worker=request.session.get("id")).exists())
    print(bool(post.branch) and post.branch.id == Branches.objects.get(worker=request.session.get("id")).id)
    if (
        request.session.get("role") == "worker"
        and Branches.objects.filter(worker=request.session.get("id")).exists()
    ):
        if bool(post.branch) and post.branch.id == Branches.objects.get(worker=request.session.get("id")).id:
            own_post = True
    print(own_post)
    return render(
        request,
        "see_ecommerce_post.html",
        {
            "post": post,
            "post_image": post_image,
            "user_session": False,
            "session_name": session_name(request),
            "session_id": request.session.get("id"),
            "own_post": own_post,
            "category": ProductCategory.objects.filter(
                id=post.product_category_id
            ).first(),
            "role": request.session.get("role"),
        },
    )
def delete_post(request, id):
    print(id)
    if EcommercePost.objects.filter(id=id).exists():
        EcommercePost.objects.filter(id=id).first().delete()
    return redirect('list_ecommerce')

def exchange_points(request, id):
    """
    docstring
    """
    pass