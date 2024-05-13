from . import views
from django.urls import path

urlpatterns = [
    path("", views.see_users, name= "see_users"),
    path("send_email/", views.send_email, name="send_email"),
    path("recover_page/", views.recover_page, name="recover_page"),
    path("recovery/", views.recovery, name="recovery"),
    path("recovery/recovered/", views.recovered, name="recovered")
]