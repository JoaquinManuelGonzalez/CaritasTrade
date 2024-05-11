from django.urls import path

from . import views

urlpatterns = [
    path('log_in_form/', views.login_view, name='log_in_form'),
    path('confirm_session/', views.confirm_session_view, name='confirm_session')
]