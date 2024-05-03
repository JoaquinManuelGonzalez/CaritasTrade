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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('landing_page/', landing_page_views.landing_page),
    path('registration_form/', affiliate_registration_views.registration_form)
]
