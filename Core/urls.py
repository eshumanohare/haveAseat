from django.urls import path
from . import views

urlpatterns = [
    path("admin-panel/", views.adminPanel, name = "adminPanel"),
    path("student-panel/", views.studentPanel, name = "studentPanel"),
    path("course-description/", views.courseDescription, name = "courseDescription"),
    path("", views.homepage, name="homepage"),
]
