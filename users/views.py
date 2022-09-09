from django.contrib.auth import authenticate

def checkUserLogin(email, password):
    user = authenticate(username=email, password=password)
    if user is not None:
        return True
    else:
        return False