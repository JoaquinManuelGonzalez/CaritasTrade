from . import views
from django.urls import path

urlpatterns = [
    path("finish_day/", views.finish_day, name="finish_day")
]