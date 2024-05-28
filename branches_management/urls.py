from django.urls import path

from . import views

urlpatterns = [
    path("branches_management/", views.list_branches, name="branches_management"),
    path("branches_management/create_branch/", views.create_branch, name="create_branch"),
    path("branches_management/edit_branch/<int:branch_id>", views.edit_branch, name="edit_branch"),
    path("branches_management/delete_branch/<int:branch_id>", views.delete_branch, name="delete_branch"),
]