from django.urls import path
from . import views

urlpatterns = [
    path("see_workers/", views.see_workers, name="see_workers"),
    path("create_worker/", views.create_worker, name="create_worker"),
    path("edit_worker/", views.edit_worker, name="edit_worker"),
    path("delete_worker/", views.delete_worker, name="delete_worker"),
]
