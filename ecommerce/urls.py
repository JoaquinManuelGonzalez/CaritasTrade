from urllib import request
from django.urls import path
from . import views

urlpatterns = [
    path('list_ecommerce/', views.list_ecommerce, name='list_ecommerce'),
    path('see_ecommerce_post/<int:id>', views.see_ecommerce_post, name='see_ecommerce_post'),
    path('delete_post/<int:id>', views.delete_post, name='delete_post'),
]
