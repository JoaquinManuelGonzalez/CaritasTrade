from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("about_us/", views.about_us, name="about_us"),
]
