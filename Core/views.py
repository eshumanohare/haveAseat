from django.shortcuts import render

def adminPanel(request):
    return render(request, "admin-panel.html", context = {})

def studentPanel(request):
    return render(request, "student-panel.html", context = {})

def courseDescription(request):
    return render(request, "course-description.html", context = {})

def homepage(request):
    return render(request, "homepage.html", context = {})
