from django.urls import path 

from . import views

urlpatterns = [
     path("/delete_post/<int:id>", views.see_post, name="see_post"),
]