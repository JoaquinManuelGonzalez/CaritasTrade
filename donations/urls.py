from django.urls import path
from . import views

urlpatterns = [
    path('', views.donation_view, name='donation_view'),
    path('success/', views.donation_success_view, name='donation_success'),
    path('failure/', views.donation_failure_view, name='donation_failure'),
    path('pending/', views.donation_pending_view, name='donation_pending'),
]
