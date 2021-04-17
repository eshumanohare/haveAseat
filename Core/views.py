import json
import datetime
from . import models
from django.db import connection, connections
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")

    return render(request, "index.html", context = {})

def createStudent(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST["username"]
            firstName = request.POST["firstName"]
            lastName = request.POST["lastName"]
            email = request.POST["email"]
            password = request.POST["password"]
            rollNumber = request.POST["rollNumber"]
            graduationYear = request.POST["graduationYear"]
            batch = request.POST["batch"]
            program = request.POST["program"]
            branch = request.POST["branch"]
            profilePicture = request.FILES["profilePicture"]

            # Creating User model for the new student
            user = User(
                username = username,
                first_name = firstName,
                last_name = lastName,
                email = email
            )

            # Setting the student's password
            user.set_password(password)
            user.save()

            # Creater UserRole model for the new student
            userRole = models.UserRole(
                user = user,
                role = "Student"
            )
            userRole.save()

            # Creating Student model for the new student
            student = models.Student(
                user = user,
                rollNumber = rollNumber,
                graduationYear = graduationYear,
                profilePicture = profilePicture,
                batch = batch,
                program = program,
                branch = models.Branch.objects.get(branchName = branch)
            )
            student.save()

            return HttpResponseRedirect("/admin-panel/")
        else:
            return render(request, "add-student.html", context = {})
    return HttpResponseRedirect("/login/")

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

def deleteStudent(request, username):
    if request.user.is_authenticated and request.method == "POST":
        cursor = connection.cursor()
        username = username
        sqlQuery = f"SELECT * FROM Core_Branch AS B, (SELECT AU.username, AU.first_name, AU.last_name, AU.email, S.rollNumber, S.batch, S.program, S.branch_id FROM Auth_User AS AU, Core_Student AS S WHERE AU.username = '{username}') AS S WHERE B.id = S.branch_id;"
        cursor.execute(sqlQuery)
        sqlQueryOutput = cursor.fetchone()
        email = sqlQueryOutput[5]
        firstName = sqlQueryOutput[3]
        lastName = sqlQueryOutput[4]
        rollNumber = sqlQueryOutput[6]
        batch = sqlQueryOutput[7]
        program = sqlQueryOutput[8]
        branch = sqlQueryOutput[1]
        
        # User.objects.get(username = username).delete()

        return JsonResponse({
            "success": True,
            "username": username,
            "email": email,
            "rollNumber": rollNumber,
            "firstName": firstName,
            "lastName": lastName,
            "branch": branch,
            "program": program,
            "batch": batch,
        })
    else:
        return JsonResponse({
            "success": False,
            "username": None,
            "firstName": None,
            "lastName": None,
            "branch": None,
            "program": None,
            "batch": None,
        })

def fetchFaculties(request):
    if request.user.is_authenticated and request.method == "POST":
        cursor = connection.cursor()
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
        cursor = connection.cursor()
        data = json.loads(request.body.decode())
        branches = data["branches"]
        years = data["years"]
        programs = data["programs"]
        print(programs, years, branches)
        branchesSQLPart = " OR ".join([f"B.branchName = '{branch}'" for branch in branches])
        programsSQLPart = " OR ".join([f"A.program = '{program}'" for program in programs])
        joiningYearsSQLPart = None

        if years[0] == "None" and years[1] == "None":
            joiningYearsSQLPart = " "
        elif years[0] == "None":
            joiningYearsSQLPart = f" A.dateOfJoining <= '{years[1]}-12-31' "
        elif years[1] == "None":
            joiningYearsSQLPart = f" A.dateOfJoining >= '{years[0]}-01-01' "
        else:
            joiningYearsSQLPart = f" A.dateOfJoining >= '{years[0]}-01-01' AND A.dateOfJoining <= '{years[1]}-12-31' "

        wherePart = ""
        whereConstraints = []

        if branchesSQLPart.strip() != "":
            whereConstraints.append("(" + branchesSQLPart + ")")

        if joiningYearsSQLPart.strip() != "":
            whereConstraints.append("(" + joiningYearsSQLPart + ")")

        if programsSQLPart.strip() != "":
            whereConstraints.append("(" + programsSQLPart + ")")

        if len(whereConstraints) > 0:
            wherePart = f" WHERE {' AND '.join(whereConstraints)}"

        if wherePart.strip() != "":
            sqlQuery = f"SELECT AU.username, AU.email, AU.first_name, AU.last_name, S.rollNumber, S.batch, S.program, S.branchName, S.dateOfJoining, S.graduationYear FROM Auth_User AS AU, (SELECT A.user_id, A.rollNumber, A.dateOfJoining, A.graduationYear, A.batch, A.program, B.branchName FROM Core_Student AS A, Core_Branch AS B {wherePart} AND (A.branch_id = B.id)) AS S where AU.id = S.user_id;"
        else:
            sqlQuery = f"SELECT AU.username, AU.email, AU.first_name, AU.last_name, S.rollNumber, S.batch, S.program, S.branchName, S.dateOfJoining, S.graduationYear FROM Auth_User AS AU, (SELECT A.user_id, A.rollNumber, A.dateOfJoining, A.graduationYear, A.batch, A.program, B.branchName FROM Core_Student AS A, Core_Branch AS B WHERE (A.branch_id = B.id)) AS S where AU.id = S.user_id;"

        print(sqlQuery)

        cursor.execute(sqlQuery)
        sqlQueryOutput = cursor.fetchall()
        print(sqlQueryOutput)

        return JsonResponse({
            "success": True,
            "outputs": studentsToListOfDictionaries(sqlQueryOutput)
        })
    return JsonResponse({
        "success": False,
    })

def fetchCourses(request):
    if request.user.is_authenticated and request.method == "POST":
        cursor = connection.cursor()
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
        result["username"] = output[0]
        result["email"] = output[1]
        result["firstName"] = output[2]
        result["lastName"] = output[3]
        result["profileLink"] = output[4]
        results.append(result)

    return results

def studentsToListOfDictionaries(outputs):
    results = []

    for output in outputs:
        result = {}
        result["username"] = output[0]
        result["email"] = output[1]
        result["firstName"] = output[2]
        result["lastName"] = output[3]
        result["rollNumber"] = output[4]
        result["batch"] = output[5]
        result["program"] = output[6]
        result["branch"] = output[7]
        result["dateOfJoining"] = output[8]
        result["graduationYear"] = output[9]
        results.append(result)

    return results

def homepage(request):
    return render(request, "homepage.html", context = {})
