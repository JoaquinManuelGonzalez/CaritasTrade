from django.urls import path

from . import views

urlpatterns = [
    path("pending_exchanges_management/", views.pending_exchanges_management, name="pending_exchanges_management"),
    path("pending_exchanges_management/accept_exchange/<int:exchange_id>", views.accept_exchange, name="accept_exchange"),
    path("pending_exchanges_management/reject_exchange/<int:exchange_id>", views.reject_exchange, name="reject_exchange")
]