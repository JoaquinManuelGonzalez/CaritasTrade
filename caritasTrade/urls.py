"""
URL configuration for caritasTrade project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from landing_page import views as landing_page_views
from affiliate_registration import views as affiliate_registration_views
from see_post import views as see_post_views
from create_post import views as create_post_views
from exchanges import views as exchanges_views
from view_map import views as view_maps_views
from select_branch import views as select_branch_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "registration_form/",
        affiliate_registration_views.registration_form,
        name="registration_form",
    ),
    path("", landing_page_views.landing_page, name="landing_page"),
    path("see_post/<int:id>/", see_post_views.see_post, name="see_post"),
    path("create_post/", create_post_views.create_post, name="create_post"),
    path("log_in/", include("log_in.urls"), name="log_in_form"),
    path(
        "list_exchange_products/",
        include("list_exchange_products.urls"),
        name="list_exchange_products",
    ),
    path("edit_profile/", include("edit_profile.urls"), name="edit_profile"),
    path("view_profile/", include("view_profile.urls"), name="view_profile"),
    path("about_us/", landing_page_views.about_us, name="about_us"),
    path("recovery_email/", include("recovery_email.urls"), name="recovery_email"),
    path("validate_post/", include("validate_post.urls"), name="validate_post"),
    path(
        "see_exchange_requests",
        exchanges_views.see_exchange_requests,
        name="see_exchange_requests",
    ),
    path(
        "send_exchange_solicitude/<int:post_id_for>",
        see_post_views.send_exchange_solicitude,
        name="send_exchange_solicitude",
    ),
    path(
        "register_exchange",
        exchanges_views.register_exchange,
        name="register_exchange",
    ),
    path(
        "validate_exchange_codes",
        exchanges_views.validate_exchange_codes,
        name="validate_exchange_codes",
    ),
    path('view_map/', view_maps_views.view_map, name='view_map'),
    path("create_worker/", include("create_worker.urls"), name="create_worker"),
    path('branches_management/', include("branches_management.urls"), name='branches_management'),
    path("categories/", include('categories.urls'), name="categories"),
    path("rate_exchange/", include("rate_exchange.urls"), name="rate_exchanges"),

    path("select_branch/<int:solicitude_id>", select_branch_views.select_branch, name="select_branch"),
    path("edit_worker/", include("edit_worker.urls"), name="edit_worker"),
    path("list_workers/", include("list_workers.urls"), name="list_worker"),
    path(
        "return_error_message_regarding_active_exchanges",
        exchanges_views.return_error_message_regarding_active_exchanges,
        name="return_error_message_regarding_active_exchanges",
    ),
    path(
        "delete_request/<int:id>",
        exchanges_views.delete_request,
        name="delete_request",
    ),
    path(
        "pending_exchanges_management/",
        include("pending_exchanges.urls"),
        name="pending_exchanges_management",
    ),
    path("finish_day/", include("finish_day.urls"), name="finish_day" ),
    path('donations/', include('donations.urls'), name="donate" ),
    path('stadistics/', include('stadistics.urls'), name="stadistics" ),
    path('favorites/', include('need_list.urls'), name="favorites"),
]
