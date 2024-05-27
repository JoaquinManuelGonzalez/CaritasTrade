from django.urls import path

from . import views

urlpatterns = [
    path("select_branch/<int:solicitude_id>", views.select_branch, name="select_branch"),
]