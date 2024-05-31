from django.urls import path
from . import views

urlpatterns = [
    path("edit_worker_profile/", views.edit_worker_profile, name="edit_worker_profile"),
]
