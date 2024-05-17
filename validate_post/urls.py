from . import views
from django.urls import path

urlpatterns = [
    path("see_waiting_posts/", views.see_waiting_posts, name="see_waiting_posts"),
    path("accept/", views.accept, name="accept"),
    path("reject/", views.reject, name="reject"),
    path("block/", views.block, name="block"),
    path("worker_block/", views.worker_block, name="worker_block"),
]
