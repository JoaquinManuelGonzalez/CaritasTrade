from django.urls import path 

from . import views

urlpatterns = [
     path("see_exchange_requests", views.see_exchange_requests, name="see_exchange_requests"),
     path("register_exchange", views.register_exchange, name="register_exchange"),
]