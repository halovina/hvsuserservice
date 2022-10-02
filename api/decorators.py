from xml.dom.minidom import Element
from internal.pyjwt import jwtDecode
from datetime import datetime
from django.http import JsonResponse
from rest_framework import status


def auth_user_token(function):
    def wrapper(request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            data = jwtDecode(token)
            if checkTokenExpired(data['expired_time']) == False:
                return JsonResponse({
                    "message":"token expired"
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({
                    "message":"not authorized"
                }, status=status.HTTP_400_BAD_REQUEST)
        return function(request, *args, **kwargs)
    return wrapper


def checkTokenExpired(expired_time):
    current_time = datetime.now()
    current_unix_time = current_time.timestamp()
    if current_unix_time <= expired_time:
        return True
    return False