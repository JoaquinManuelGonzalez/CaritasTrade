from django.urls import path

from . import views

urlpatterns = [
    path("branches_management/", views.list_branches, name="branches_management"),
    path("branches_management/create_branch/", views.create_branch, name="create_branch")
]