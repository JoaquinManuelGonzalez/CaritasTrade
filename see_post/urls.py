from django.urls import path

from . import views

urlpatterns = [
    path("/see_post/<int:id>", views.see_post, name="see_post"),
]
