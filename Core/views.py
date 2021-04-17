import json
import datetime
from django.db import connection
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *

cursor = connection.cursor()

############################### sql queries using api #############################

# create queries

def createCourses():
     # creating an object
        courseobj = Course(1, 'A', 'Introduction To Programming', 4,100,'Introduction of Programming is the first programming course in the college curriculum, and aims to bridge the gap between students who have prior coding experience and those who have none. The main goal of this course is to prepare students to understand basic algorithms and data structures, write organized code, and to gain practical experience with debugging, compiling and running programs.', 'B-Tech', 1, 1)

        # object.save() executes the insert query into the database
        courseobj.save()

        courseobj1 = Course(2, 'B', 'Machine Learning', 4,200,'This is an introductory course on Machine Learning (ML) that is offered to undergraduate and graduate students. The contents are designed to cover both theoretical and practical aspects of several well-established ML techniques. The assignments will contain theory and programming questions that help strengthen the theoretical foundations as well as learn how to engineer ML solutions to work on simulated and publicly available real datasets. The project(s) will require students to develop a complete Machine Learning solution requiring preprocessing, design of the classifier/regressor, training and validation, testing and evaluation with quantitative performance comparisons.', 'B-Tech', 2, 0)

        courseobj1.save()

        courseobj2 = Course(3, 'A', 'Algorithm Design & Analysis', 4,120,'This is a follow-up course to DSA (Data Structures and Algorithms). The focus of this course in on the design of algorithms, proofs of correctness and methods to analyse resource requirements of their algorithms. Students learn fundamental algorithmic design paradigms such as greedy algorithms, dynamic programming, divide and conquer, etc. and also learn some more data structures. The later part of the course focuses on the limitations of algorithms. In particular, the theory of NP-completeness. Students are also required to design and implement algorithms using the techniques the learn.', 'B-Tech', 3, 0)

        courseobj2.save()

        courseobj3 = Course(4, 'B', 'Data Structures & Algorithms', 4,220,'This course is aimed at giving students a background in basic data structures and algorithms along with their impact in solving real life problems using a computer. The major focus will be on covering the basic data structures, b) Algorithm analysis using recurrence relations and c) problem solving using Java', 'B-Tech', 4, 0)

        courseobj3.save()

        courseobj4 = Course(5, 'A', 'Statistics', 4,100,'This course is aimed at giving students a background in basic data structures and algorithms along with their impact in solving real life problems using a computer. The major focus will be on covering the basic data structures, b) Algorithm analysis using recurrence relations and c) problem solving using Java', 'M-Tech', 3, 0)

        courseobj4.save()

        courseobj5 = Course(6, 'B', 'Genomic Algorithms', 2,50,'This course is aimed at giving students a background in basic data structures and algorithms along with their impact in solving real life problems using a computer. The major focus will be on covering the basic data structures, b) Algorithm analysis using recurrence relations and c) problem solving using Java', 'PhD', 1, 1)

        courseobj5.save()

        courseobj6 = Course(7, 'A', 'Iski Topi Uske Sir', 2,10,'This course is aimed at giving students a background in basic data structures and algorithms along with their impact in solving real life problems using a computer. The major focus will be on covering the basic data structures, b) Algorithm analysis using recurrence relations and c) problem solving using Java', 'M-Tech', 4, 1)

        courseobj6.save()

        courseList = [courseobj, courseobj1,courseobj2,courseobj3,courseobj4,courseobj5,courseobj6]

        return courseList

def createDepartment():
    dep1 = Department(1,"CSE")
    dep1.save()
    dep2 = Department(2,"ECE")
    dep2.save()
    dep3 = Department(3,"MTH")
    dep3.save()
    dep4 = Department(4,"SSH")
    dep4.save()

    dList = [dep1,dep2,dep3,dep4]
    return dList

####### calls for creating #####
depList = createDepartment()
######## global lists ##########
courseList = []

def createPreReq():
    pre1 = PreReq(1,2,1)
    pre1.save()
    pre2 = PreReq(2,2,5)
    pre2.save()
    pre3 = PreReq(3,3,1)
    pre3.save()
    pre4 = PreReq(4,3,4)
    pre4.save()
    pre5 = PreReq(5,4,1)
    pre5.save()

    preList = [pre1,pre2,pre3,pre4,pre5]
    return preList

######## for preReq ###########
# preReqList = createPreReq()

# insert course from admin panel
def insertCourseAdmin(request):
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username = username)
        role = UserRole.objects.get(user=user)
        if request.method == "POST" and role.role=='admin':
            department = Department.objects.get(departmentName = request.POST.get('department'))
            newCourse = Course(id = request.POST.get('id'), section = request.POST.get('section'), courseName = request.POST.get('courseName'), credits = request.POST.get('credits'), studentCap = request.POST.get('studentCap'), courseDescription = request.POST.get('courseDescription'), program = request.POST.get('program'), department = department, isLive = 0)
            newCourse.save()
            print("Saved")
        return HttpResponseRedirect("/"+role.role+"-panel")
    return HttpResponseRedirect("/")


######################################### Updation queries ##############################

# update studentCap in a Course from admin-panel
def updateCap(request):
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username = username)
        role = UserRole.objects.get(user=user)
        if request.method == "POST" and role.role=='admin':
            course = Course.objects.get(id = request.POST.get('id'))
            course.studentCap = request.POST.get('studentCap')
            course.save()
            print("Course cap is updated.")
        return HttpResponseRedirect("/"+role.role+"-panel")
    return HttpResponseRedirect("/")

# make isLive=1 courses
# make Course Live from Admin Panel
def setisLive1(request):
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username = username)
        role = UserRole.objects.get(user=user)
        if request.method == "POST" and role.role=='admin':
            course = Course.objects.get(id = request.POST.get('id'))
            course.isLive=1
            course.save()
            print("Course is live.")
        return HttpResponseRedirect("/"+role.role+"-panel")
    return HttpResponseRedirect("/")

# make isLive=0 courses
# make Course Inactive from Admin Panel
def setisLive0(request):
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username = username)
        role = UserRole.objects.get(user=user)
        if request.method == "POST" and role.role=='admin':
            course = Course.objects.get(id = request.POST.get('id'))
            course.isLive=0
            course.save()
            print("Course has been removed from live courses.")
        return HttpResponseRedirect("/"+role.role+"-panel")
    return HttpResponseRedirect("/")

# delete queries

# delete courses from student panel
def deleteCourses(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            # courseList = createCourses()
            snos = request.POST.getlist("courseList")
            print(snos)
            for i in snos:
                courseObject = Course.objects.filter(id=i)
                # print(courseObject[0].id)
                for course in courseList:
                    if len(courseObject) != 0 and course.id == courseObject[0].id:
                        print(course.id)
                        courseList.remove(course)
                
                courseObject.delete()

            context = {'courseList': courseList}
            return render(request, "student-panel.html", context)
    else:
        return HttpResponseRedirect("/")

# delete course from admin panel
def deleteCourseAdmin(request):
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username = username)
        role = UserRole.objects.get(user=user)
        if request.method == "POST" and role.role=='admin':
            course = Course.objects.get(id = request.POST.get('id'))
            course.delete()
            print("Deleted")
        return HttpResponseRedirect("/"+role.role+"-panel")
    return HttpResponseRedirect("/")


# read queries
def filterCourses(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            checkBtech = request.POST.get("B-Tech")
            checkMtech = request.POST.get("M-Tech")
            checkPhD = request.POST.get("PhD")
            
            # print(type(checkBtech))

            check4 = request.POST.get("cred4")
            check2 = request.POST.get("cred2")

            filteredCourses = []

            if checkBtech == None and checkMtech == None and checkPhD == None:
                querySet = Course.objects.filter(credits__in = [check4,check2])
            else:
                if check4 == None and check2 == None:
                    querySet = Course.objects.filter(program__in = [checkBtech,checkMtech,checkPhD])
                else:
                    querySet = Course.objects.filter(program__in = [checkBtech,checkMtech,checkPhD],credits__in = [check4,check2])
            # print(querySet)

            for i in range(0,len(querySet)):
                print(querySet[i].courseName)
                filteredCourses.append(querySet[i])

            context = {'courseList': filteredCourses}

            return render(request,"student-panel.html", context)
    else:
        return HttpResponseRedirect("/")


########################## queries using api ends ############################
def getAllCourses(request):
    context = {
        'courseList': courseList,
    }
    return render(request,'student-panel.html',context)


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")

    return render(request, "index.html", context = {})

def loginView(request):
    if request.user.is_authenticated is False:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            role = request.POST.get("role")

            # Authenticating the user
            user = authenticate(username = username, password = password)

            if user is not None:
                login(request, user) # Logging in the user
                print(f"{user.username} logged in successfully!")
                # send_mail(
                #     subject = f"{user.username}, you just logged in with your account on www.haveASeat.com",
                #     message = f"You logged in using your account on {datetime.date.today().strftime('%d %B, %Y, %A')} at {datetime.datetime.now().time().strftime('%H:%M:%S %p')}.",
                #     from_email = settings.EMAIL_HOST_USER,
                #     recipient_list = [user.email]
                # )
                return HttpResponseRedirect("/"+role+"-panel")
            else:
                return render(request, "login.html", context = {
                    "messages": [
                        [
                            "User doesn't exists",
                            "The credentials enter are incorrect. Please try again with valid credentials of create an account."
                        ],
                    ]
                })        

                return HttpResponseRedirect("/")

        return render(request, "login.html", context = {})
    
    return HttpResponseRedirect("/")

def createAccount(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            email = request.POST.get("email")
            role = request.POST.get("role")
            user = User(
                username = username,
                email = email
            )
            user.set_password(password)
            user.save()
            userRole = UserRole(
                user = user,
                role = role
            )
            userRole.save()
            print(f" Username -> {username}")
            print(f" Email -> {email}")
            print(f" Password -> {password}")
            print(f" Role -> {role}")
            # send_mail(
            #         subject = f"Welcome to www.haveASeat.com, {user.username}",
            #         message = f"Your account on www.haveASeat.com was successfully created {datetime.date.today().strftime('%d %B, %Y, %A')} at {datetime.datetime.now().time().strftime('%H:%M:%S %p')}.",
            #         from_email = settings.EMAIL_HOST_USER,
            #         recipient_list = [user.email]
            #     )

            return HttpResponseRedirect("/login")

        return render(request, "create-account.html", context = {})

    return HttpResponseRedirect("/")

def adminPanel(request):
    if request.user.is_authenticated:
        courses=Course.objects.all()
        context = {
            'courseList': courses,
        }
        return render(request, "admin-panel.html", context)
    else:
        return HttpResponseRedirect("/")

def studentPanel(request):
    # for i in courseList:
    #     print(i.courseName)

    cList = Course.objects.all()
    courses = []
    for i in cList:
        courses.append(i)

    if request.user.is_authenticated:
        context = {
            'courseList': courses
        }
        return render(request, "student-panel.html", context)
    else:
        return HttpResponseRedirect("/")

# def courseDescription(request, course_courseName):
#     if request.user.is_authenticated:
#         course = Course.objects.get(courseName = course_courseName)
#         preList = []
#         for i in preReqList:
#             if i.course_id == course.id :
#                 preList.append(i.preReqCourse)
#         context = {
#             'course': course,
#             'preReq': preList,
#             'depList': depList
#         }
#         return render(request, "course-description.html", context)
#     else:
#         return HttpResponseRedirect("/")

def logoutView(request):
    if request.user.is_authenticated:
        logout(request) # Logging out the user
        print(f"{request.user.username} logged out successfully!")

    return HttpResponseRedirect("/")

def fetchFaculties(request):
    if request.user.is_authenticated and request.method == "POST":
        data = json.loads(request.body.decode("UTF-8"))
        programs = data["programs"]
        departments = data["departments"]
        print(programs, departments)
        programsSQLPart = " OR ".join([f"C.program = '{program}'" for program in programs])
        departmentsSQLPart = " OR ".join([f"D.departmentName = '{department}'" for department in departments])        
        wherePart = ""
        whereConstraints = []

        if programsSQLPart.strip() != "":
            whereConstraints.append("(" + programsSQLPart + ")")

        if departmentsSQLPart.strip() != "":
            whereConstraints.append("(" + departmentsSQLPart + ")")

        if len(whereConstraints) > 0:
            wherePart = f" WHERE {' AND '.join(whereConstraints)}"

        print(wherePart)

        if wherePart.strip() != "":
            sqlQuery = f"SELECT AU.username, AU.email, AU.first_name, AU.last_name, F.profileLink FROM Auth_User AS AU, (SELECT F.user_id, F.profileLink FROM Core_Faculty AS F, (SELECT DISTINCT CF.faculty_id FROM Core_CourseFaculty AS CF, (SELECT C.id FROM Core_Course AS C, Core_Department AS D {wherePart}) AS CC WHERE CF.course_id = CC.id) AS CF WHERE CF.faculty_id = F.id) AS F where AU.id = F.user_id;"
        else:
            sqlQuery = f"SELECT AU.username, AU.email, AU.first_name, AU.last_name, F.profileLink FROM Auth_User AS AU, (SELECT F.user_id, F.profileLink FROM Core_Faculty AS F, (SELECT DISTINCT CF.faculty_id FROM Core_CourseFaculty AS CF, (SELECT C.id FROM Core_Course AS C, Core_Department AS D) AS CC WHERE CF.course_id = CC.id) AS CF WHERE CF.faculty_id = F.id) AS F where AU.id = F.user_id;"

        print(sqlQuery)

        cursor.execute(sqlQuery)
        sqlQueryOutput = cursor.fetchall()
        print(sqlQueryOutput)

        return JsonResponse({
            "success": True,
            "outputs": facultiesToListOfDictionaries(sqlQueryOutput)
        })

    return JsonResponse({
        "success": False,
    })

def fetchStudents(request):
    if request.user.is_authenticated and request.method == "POST":
        data = json.loads(request.body.decode())

def fetchCourses(request):
    if request.user.is_authenticated and request.method == "POST":
        data = json.loads(request.body.decode("UTF-8"))
        sections = data["sections"]
        courseCredits = data["credits"]
        programs = data["programs"]
        departments = data["departments"]
        print(sections, courseCredits, programs, departments)
        semestersSQLPart = " OR ".join([f"A.section = '{section}'" for section in sections])
        creditsSQLPart = " OR ".join([f"A.credits = {courseCredit}" for courseCredit in courseCredits])
        programsSQLPart = " OR ".join([f"A.program = '{program}'" for program in programs])
        departmentsSQLPart = " OR ".join([f"A.departmentName = '{department}'" for department in departments])        
        wherePart = ""
        whereConstraints = []

        if creditsSQLPart.strip() != "":
            whereConstraints.append("(" + creditsSQLPart + ")")

        if semestersSQLPart.strip() != "":
            whereConstraints.append("(" + semestersSQLPart + ")")

        if programsSQLPart.strip() != "":
            whereConstraints.append("(" + programsSQLPart + ")")

        if departmentsSQLPart.strip() != "":
            whereConstraints.append("(" + departmentsSQLPart + ")")

        if len(whereConstraints) > 0:
            wherePart = f" WHERE {' AND '.join(whereConstraints)}"

        print(whereConstraints)
        print(wherePart)

        if wherePart.strip() != "":
            sqlQuery = f"SELECT A.section, A.courseName, A.credits, A.studentCap, A.program, A.departmentName FROM (SELECT * FROM Core_Course AS CC, Core_Department AS CD WHERE CC.department_id = CD.id) AS A {wherePart};"
        else:
            sqlQuery = f"SELECT A.section, A.courseName, A.credits, A.studentCap, A.program, A.departmentName FROM (SELECT * FROM Core_Course AS CC, Core_Department AS CD WHERE CC.department_id = CD.id) AS A;"

        print(sqlQuery)

        cursor.execute(sqlQuery)
        sqlQueryOutput = cursor.fetchall()

        return JsonResponse({
            "success": True,
            "outputs": coursesToListOfDictionaries(sqlQueryOutput)
        })

    return JsonResponse({
        "success": False,
    })

def coursesToListOfDictionaries(outputs):
    results = []

    for output in outputs:
        result = {}
        result["section"] = output[0]
        result["courseName"] = output[1]
        result["credits"] = output[2]
        result["studentCap"] = output[3]
        result["program"] = output[4]
        result["department"] = output[5]
        results.append(result)

    return results

def facultiesToListOfDictionaries(outputs):
    results = []

    for output in outputs:
        result = {}
        [('admin', 'admin@gmail.com', 'Admin', 'Ji', 'https://www.instagram.com/itsmrvaibhav')]
        result["username"] = output[0]
        result["email"] = output[1]
        result["firstName"] = output[2]
        result["lastName"] = output[3]
        result["profileLink"] = output[4]
        results.append(result)

    return results
    return render(request, "course-description.html", context = {})

def homepage(request):
    return render(request, "homepage.html", context = {})
