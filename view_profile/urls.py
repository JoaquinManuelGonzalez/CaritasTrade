from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("user/<int:id>", views.profile, name="view_profile"),
    path("confirm_sign_off/", views.confirm_sign_off, name="confirm_sign_off"),
    path("delete_post/<int:id>", views.delete_post, name="delete_post"),
]
