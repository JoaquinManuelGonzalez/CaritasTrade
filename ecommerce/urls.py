from urllib import request
from django.urls import path
from . import views

urlpatterns = [
    path("list_ecommerce/", views.list_ecommerce, name="list_ecommerce"),
    path(
        "see_ecommerce_post/<int:id>",
        views.see_ecommerce_post,
        name="see_ecommerce_post",
    ),
    path("delete_post/<int:id>", views.delete_post, name="delete_post"),
    path("create_eccomerce_post/", views.create_eccomerce_post, name="create_eccomerce_post"),
    path("exchange_points/<int:id>", views.exchange_points, name="exchange_points"),
    path("see_cupons/", views.see_cupons, name="see_cupons"),
    path("download_cupon/<int:cupon_id>/", views.download_cupon, name="download_cupon"),
    path("register_cupons/", views.register_cupons, name="register_cupons"),
    path("see_ecommerce_post/", views.see_ecommerce_post, nam="see_ecommerce_post"),
    path("edit_eccomerce_post/<int:id>/", views.edit_eccomerce_post, name="edit_eccomerce_post")
]
