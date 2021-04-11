from django.db import models
from django.contrib.auth.models import User
from django.db import connection

class Branch(models.Model):
    branchName = models.CharField(max_length = 100)

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"

class Department(models.Model):
    departmentName = models.CharField(max_length = 100)

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"

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
    profilePicture = models.ImageField(upload_to = "Profile Pictures/Faculties/")
    profielLink = models.URLField()

    class Meta:
        verbose_name = "Faculty"
        verbose_name_plural = "Faculties"

class Course(models.Model):
    code = models.CharField(max_length=7, null=True,default="")
    section = models.CharField(max_length = 3)
    courseName = models.CharField(max_length = 50)
    credits = models.IntegerField(default = 0)
    studentCap = models.IntegerField(default = 0)
    courseDescription = models.TextField()
    program = models.CharField(max_length = 50)

class has_pre_req(models.Model):
    from_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="from_course")
    to_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="to_course")

class has_anti_req(models.Model):
    from_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="anti_from_course")
    to_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="anti_to_course")

class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)