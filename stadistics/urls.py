from . import views
from django.urls import path

urlpatterns = [
    path("", views.main_view, name="main_view"),
    path(
        "transactions/pie-chart/",
        views.transactions_pie_chart,
        name="transactions_pie_chart",
    ),
    path("transactions/by-age/", views.transactions_by_age, name="transactions_by_age"),
    path(
        "transactions/by-age/<str:age_range>/",
        views.transactions_by_age,
        name="transactions_by_age_range",
    ),
    path("category-histogram/", views.category_histogram, name="category_histogram"),
]
