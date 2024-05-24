from django.urls import path

from . import views

urlpatterns = [
    path("/see_post/<int:id>", views.see_post, name="see_post"),
    path("/get_user_posts/<int:id>", views.get_posts_from_user, name="get_user_posts"),
]
