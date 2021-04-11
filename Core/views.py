from django.shortcuts import render
from django.db import connection
from .models import *

def adminPanel(request):
    return render(request, "admin-panel.html", context = {})

def studentPanel(request):

    # creating an object
    courseobj = Course(1,'CSE101', 'A', 'Introduction To Programming', 4,100,'Introduction of Programming is the first programming course in the college curriculum, and aims to bridge the gap between students who have prior coding experience and those who have none. The main goal of this course is to prepare students to understand basic algorithms and data structures, write organized code, and to gain practical experience with debugging, compiling and running programs.', 'B-Tech')
    
    # object.save() executes the insert query into the database
    courseobj.save()

    courseobj1 = Course(2,'CSE343', 'B', 'Machine Learning', 4,200,'This is an introductory course on Machine Learning (ML) that is offered to undergraduate and graduate students. The contents are designed to cover both theoretical and practical aspects of several well-established ML techniques. The assignments will contain theory and programming questions that help strengthen the theoretical foundations as well as learn how to engineer ML solutions to work on simulated and publicly available real datasets. The project(s) will require students to develop a complete Machine Learning solution requiring preprocessing, design of the classifier/regressor, training and validation, testing and evaluation with quantitative performance comparisons.', 'B-Tech')
    
    courseobj1.save()

    courseobj2 = Course(3,'CSE222', 'A/B', 'Algorithm Design & Analysis', 4,120,'This is a follow-up course to DSA (Data Structures and Algorithms). The focus of this course in on the design of algorithms, proofs of correctness and methods to analyse resource requirements of their algorithms. Students learn fundamental algorithmic design paradigms such as greedy algorithms, dynamic programming, divide and conquer, etc. and also learn some more data structures. The later part of the course focuses on the limitations of algorithms. In particular, the theory of NP-completeness. Students are also required to design and implement algorithms using the techniques the learn.', 'B-Tech')
    
    courseobj2.save()

    courseobj3 = Course(4,'CSE102', 'A/B', 'Data Structures & Algorithms', 4,220,'This course is aimed at giving students a background in basic data structures and algorithms along with their impact in solving real life problems using a computer. The major focus will be on covering the basic data structures, b) Algorithm analysis using recurrence relations and c) problem solving using Java', 'B-Tech')
        
    courseobj3.save()

    courseList= {courseobj, courseobj1, courseobj2, courseobj3}
    
    context = {
        'courseList': courseList
    }
    return render(request, "student-panel.html", context)

def courseDescription(request):
    return render(request, "course-description.html", context = {})

def homepage(request):
    return render(request, "homepage.html", context = {})
