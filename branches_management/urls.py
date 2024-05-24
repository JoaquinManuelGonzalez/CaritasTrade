from django.urls import path

from . import views

urlpatterns = [
    path("branches_management/", views.list_branches, name="branches_management")
]