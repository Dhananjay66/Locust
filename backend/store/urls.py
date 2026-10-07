from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("products/", views.product_list),
    path("products/<int:pk>/", views.product_detail),
    path("login/", views.login_view),
    path("profile/", views.profile),
    path("login-page/", views.login_page),
]