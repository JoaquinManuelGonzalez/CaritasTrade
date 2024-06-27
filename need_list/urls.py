from django.urls import path

from . import views

urlpatterns = [
    path("favorites/", views.list_favorites_products, name="favorites"),
    path("add_to_favorites/<int:post_id>", views.add_to_favorites, name="add_to_favorites"),
    path("delete_from_favorites/<int:post_id>", views.delete_from_favorites, name="delete_from_favorites"),
]