from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "Core"

urlpatterns = [
    # path("", views.homepage, name = "homepage"),
    path("", views.index, name = "index"),
    path("login/", views.loginView, name = "login"),
    path("logout/", views.logoutView, name = "logout"),
    path("create-account/", views.createAccount, name = "createAccount"),
    # path("create-student/", views.createStudent, name = "createStudent"),
    path("admin-panel/", views.adminPanel, name = "adminPanel"),
    # path("admin-panel/delete-student/<str:username>/", views.deleteStudent, name = "deleteStudent"),
    path("student-panel/", views.studentPanel, name = "studentPanel"),
    path("course-description/", views.courseDescription, name = "courseDescription"),
    path("fetch-courses/", views.fetchCourses, name = "fetchCourses"),
    path("fetch-faculties/", views.fetchFaculties, name = "fetchFaculties"),
    path("fetch-students/", views.fetchStudents, name = "fetchStudents"),
    path("delete-courses/",views.deleteCourses, name="deleteCourses"),
    path("filter-courses/",views.filterCourses,name="filterCourses"),
    path("insert-course-admin/",views.insertCourseAdmin,name="insertCourseAdmin"),
    path("delete-course-admin/",views.deleteCourseAdmin,name="deleteCourseAdmin"),
    path("set-isLive-1-admin/",views.setisLive1,name="setisLive1"),
    path("set-isLive-0-admin/",views.setisLive0,name="setisLive0"),
    path('getAllCourses/',views.getAllCourses,name='getAllCourses'),
    path("<course_courseName>/",views.courseDescription,name="courseDescription"),
]

urlpatterns += static(
    settings.MEDIA_URL, 
    document_root = settings.MEDIA_ROOT
)