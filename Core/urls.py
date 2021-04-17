from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "Core"

urlpatterns = [
    path("", views.homepage, name = "homepage"),
    path("", views.index, name = "index"),
    path("login/", views.loginView, name = "login"),
    path("logout/", views.logoutView, name = "logout"),
    path("create-account/", views.createAccount, name = "createAccount"),
    path("create-student/", views.createStudent, name = "createStudent"),
    path("admin-panel/", views.adminPanel, name = "adminPanel"),
    path("admin-panel/delete-student/<str:username>/", views.deleteStudent, name = "deleteStudent"),
    path("student-panel/", views.studentPanel, name = "studentPanel"),
    path("course-description/", views.courseDescription, name = "courseDescription"),
    path("fetch-courses/", views.fetchCourses, name = "fetchCourses"),
    path("fetch-faculties/", views.fetchFaculties, name = "fetchFaculties"),
    path("fetch-students/", views.fetchStudents, name = "fetchStudents"),
]

urlpatterns += static(
    settings.MEDIA_URL, 
    document_root = settings.MEDIA_ROOT
)