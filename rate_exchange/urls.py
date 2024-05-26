from django.urls import path
from . import views

urlpatterns = [
    path('', views.rate_list, name='rate_list'),
    path('rate_Affiliate', views.rate_affiliate, name='rate_Affiliate'),
]