from . import views
from django.urls import path

urlpatterns = [
    path("see_waiting_posts/", views.see_waiting_posts, name= "see_waiting_posts"),
]