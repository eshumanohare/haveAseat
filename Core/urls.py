from django.urls import path
from . import views

urlpatterns = [
    path("admin-panel/", views.adminPanel, name = "adminPanel"),
]