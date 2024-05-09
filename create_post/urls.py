from django.urls import path 

from . import views

urlpatterns = [
     path("/create_post/", views.see_post, name="see_post"),
]
