from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/edit/<int:id>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:id>/', views.category_delete, name='category_delete'),
    path('categories/delete_all/', views.category_delete_all, name='category_delete_all'),
]
