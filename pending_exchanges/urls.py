from django.urls import path

from . import views

urlpatterns = [
    path("pending_exchanges_management/", views.pending_exchanges_management, name="pending_exchanges_management"),
]