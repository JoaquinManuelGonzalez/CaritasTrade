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
from django.urls import path
from landing_page import views as landing_page_views
from affiliate_registration import views as affiliate_registration_views
from see_post import views as see_post_views
from create_post import views as create_post_views
from log_in import views as log_in_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration_form/', affiliate_registration_views.registration_form, name='registration_form'),
    path('', landing_page_views.landing_page, name='landing_page'),
    path('see_post/<int:id>/', see_post_views.see_post, name='see_post'),
    path('create_post/',create_post_views.create_post, name='create_post'),
    path('log_in/', log_in_views.login_view, name='log_in')
]
