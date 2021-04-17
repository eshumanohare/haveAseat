from django.db import models
from django.contrib.auth.models import User

class Branch(models.Model):
    branchName = models.CharField(max_length = 100)

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.branchName

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    role = models.CharField(max_length = 50)

    class Meta:
        verbose_name = "UserRole"
        verbose_name_plural = "UserRoles"

class Department(models.Model):
    departmentName = models.CharField(max_length = 100)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.departmentName

class Admin(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    profilePicture = models.ImageField(upload_to = "Profile Pictures/Admins/")
    program = models.CharField(max_length = 50)    

    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"

class Student(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    rollNumber = models.IntegerField(unique = True)
    dateOfJoining = models.DateField(auto_now = True)
    graduationYear = models.IntegerField(null = False, blank = False)
    profilePicture = models.ImageField(upload_to = "Profile Pictures/Students/")
    batch = models.CharField(max_length = 50)
    program = models.CharField(max_length = 50)
    branch = models.ForeignKey(Branch, on_delete = models.SET_NULL, null = True, blank = True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

class DOAA(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    profilePicture = models.ImageField(upload_to = "Profile Pictures/DOAA/")

    class Meta:
        verbose_name = "DOAA"
        verbose_name_plural = "DOAA"

class Faculty(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    profilePicture = models.ImageField(upload_to = "Profile Pictures/Faculties/")
    profileLink = models.URLField()

    class Meta:
        verbose_name = "Faculty"
        verbose_name_plural = "Faculties"

class Course(models.Model):
    section = models.CharField(max_length = 1)
    courseName = models.CharField(max_length = 50)
    credits = models.IntegerField(default = 0)
    studentCap = models.IntegerField(default = 0)
    courseDescription = models.TextField()
    program = models.CharField(max_length = 50)
    department = models.ForeignKey(Department, on_delete = models.SET_NULL, null = True)

class CourseFaculty(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete = models.CASCADE, related_name = "teaches")
    course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = "taughtBy")    

    class Meta:
        verbose_name = "CourseFaculty"
        verbose_name_plural = "CourseFaculties"

class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    timeStamp = models.DateTimeField(auto_now = True)
    content = models.CharField(max_length = 500)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    timeStamp = models.DateTimeField(auto_now = True)
    content = models.CharField(max_length = 500)
    parentComment = models.ForeignKey("Comment", related_name = "parentOf", on_delete = models.SET_NULL, null = True)

class PreReq(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = "preReqs")
    preReqCourse = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = "preReqOf")

    class Meta:
        verbose_name = "PreReq"
        verbose_name_plural = "PreReqs"

class AntiReq(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = "antiReqs")
    antiReqCourse = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = "antiReqOf")

    class Meta:
        verbose_name = "AntiReq"
        verbose_name_plural = "AntiReqs"