from django.shortcuts import render

def adminPanel(request):
    return render(request, "admin-panel.html", context = {})