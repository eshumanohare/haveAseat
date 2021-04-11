import json
import datetime
from django.db import connection
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

cursor = connection.cursor()

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")

    return render(request, "index.html", context = {})

def loginView(request):
    if request.user.is_authenticated is False:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            # Authenticating the user
            user = authenticate(username = username, password = password)

            if user is not None:
                login(request, user) # Logging in the user
                print(f"{user.username} logged in successfully!")
                send_mail(
                    subject = f"{user.username}, you just logged in with your account on www.haveASeat.com",
                    message = f"You logged in using your account on {datetime.date.today().strftime('%d %B, %Y, %A')} at {datetime.datetime.now().time().strftime('%H:%M:%S %p')}.",
                    from_email = settings.EMAIL_HOST_USER,
                    recipient_list = [user.email]
                )

                return HttpResponseRedirect("/")
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
            print(f" Username -> {username}")
            print(f" Email -> {email}")
            print(f" Password -> {password}")
            print(f" Role -> {role}")
            send_mail(
                    subject = f"Welcome to www.haveASeat.com, {user.username}",
                    message = f"Your account on www.haveASeat.com was successfully created {datetime.date.today().strftime('%d %B, %Y, %A')} at {datetime.datetime.now().time().strftime('%H:%M:%S %p')}.",
                    from_email = settings.EMAIL_HOST_USER,
                    recipient_list = [user.email]
                )

            return HttpResponseRedirect("/login")

        return render(request, "create-account.html", context = {})

    return HttpResponseRedirect("/")

def adminPanel(request):
    if request.user.is_authenticated:
        return render(request, "admin-panel.html", context = {
            "range": range(100),
        })
    else:
        return HttpResponseRedirect("/")

def studentPanel(request):
    if request.user.is_authenticated:
        return render(request, "student-panel.html", context = {})
    else:
        return HttpResponseRedirect("/")

def courseDescription(request):
    if request.user.is_authenticated:
        return render(request, "course-description.html", context = {})
    else:
        return HttpResponseRedirect("/")

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
