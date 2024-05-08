from django.urls import path

from . import views

urlpatterns = [
    path('log_in/', views.log_in, name='registration_form')
]