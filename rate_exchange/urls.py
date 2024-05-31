from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_pending_score, name='view_pending_score'),
    path('submit_score/<int:reputation_id>/', views.submit_score, name='submit_score'),
]