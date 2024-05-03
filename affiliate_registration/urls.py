from django.urls import path

from . import views

urlpatterns = [
    path('registration_form/', views.registration_form, name='registration_form')
]
