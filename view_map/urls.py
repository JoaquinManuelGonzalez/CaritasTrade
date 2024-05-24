from django.urls import path

from . import views

urlpatterns = [
    path('view_map/', views.view_map, name='view_map'),
]