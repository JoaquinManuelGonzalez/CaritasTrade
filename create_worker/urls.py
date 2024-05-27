from django.urls import path

from . import views

urlpatterns = [
    path("registration_form_worker/", views.registration_form_worker, name="registration_form_worker")
]
