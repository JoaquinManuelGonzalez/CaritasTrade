from django.urls import path

from . import views
from need_list.views import add_to_favorites

urlpatterns = [
    path("/see_post/<int:id>", views.see_post, name="see_post"),
    path("/send_exchange_solicitude/<int:post_id_for>", views.send_exchange_solicitude, name="send_exchange_solicitude")
]
