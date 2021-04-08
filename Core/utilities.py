from django.contrib.auth.models import User
from django.http import JsonResponse

def checkUsernameUniqueness(request, username):
    """
    A function to check uniqueness of a username. In other words, a function to check if the username exists in the database or not.
    """
    try:
        user = User.objects.get(username = username)

        return JsonResponse({
            "unique": False,
        })
    except:
        return JsonResponse({
            "unique": True,
        })

def checkEmailUniqueness(request, email):
    """
    A function to check uniqueness of an email. In other words, a function to check if the email exists in the database or not.
    """
    try:
        user = User.objects.get(email = email)
        
        return JsonResponse({
            "unique": False,
        })
    except:
        return JsonResponse({
            "unique": True,
        })