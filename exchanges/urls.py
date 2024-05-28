from django.urls import path 

from . import views

urlpatterns = [
     path("see_exchange_requests", views.see_exchange_requests, name="see_exchange_requests"),
     path("register_exchange", views.register_exchange, name="register_exchange"),
     path("validate_exchange_codes", views.validate_exchange_codes, name="validate_exchange_codes"),
     path("return_error_message_regarding_active_exchanges", views.return_error_message_regarding_active_exchanges, name="return_error_message_regarding_active_exchanges"),
     path("delete_request/<int:id>", views.delete_request, name="delete_request"),
]