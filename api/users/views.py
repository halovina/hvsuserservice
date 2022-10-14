from datetime import datetime
from rest_framework.views import APIView
from api.serializers import LoginSerializer, RegisterNewUserSerializer
from rest_framework.parsers import JSONParser
from users.views import checkUserLogin, create_register_user
from django.http import JsonResponse
from internal.pyjwt import jwtEncode
from django.utils import timezone
from users.views import validate_token_url, activate_account_user

class LoginView(APIView):
    def post(self, *args, **kwargs):
        try:
            data = JSONParser().parse(self.request)
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                if checkUserLogin(data['email'],data['password']):
                    current_time = datetime.now()
                    current_unix_time = current_time.timestamp()
                    expired_time = current_unix_time + (100 * 60)
                    token = jwtEncode({
                        "email": data['email'],
                        "time": timezone.now().strftime("%Y-%m-%d %H:%M:%S %z"),
                        "expired_time": expired_time
                    })
                    return JsonResponse(data = {
                        "message": "Sucess",
                        "token": token
                    }, status=200)
                else:
                    return JsonResponse(data = {
                                "message": "Cek user dan password Anda "
                            }, status=400)
            else:
                return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            print(str(e))
            return JsonResponse(data = {
                            "message": str(e)
                        }, status=400)
            
class RegisterNewUserView(APIView):
    def post(self, *args, **kwargs):
        try:
            data = JSONParser().parse(self.request)
            serializer = RegisterNewUserSerializer(data=data)
            if serializer.is_valid():
                resp = create_register_user(data)
                return JsonResponse(data = resp, status=200)
            else:
                return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse(data = {
                            "message": str(e)
                        }, status=400)
            
class UserLinkActivationView(APIView):
    def get(self,request, token, *args, **kwargs):
        try:
            status, message = validate_token_url(token)
            if status == True:
                status, message = activate_account_user(token)
                if status == False:
                    resp = {
                        'message': message,
                        'status': '-1'
                    }
                    return JsonResponse(data = resp, status=200)
                resp = {
                    'message': "user activation success",
                    'status': '00'
                }
                return JsonResponse(data = resp, status=200)
            else:
                resp = {
                    'message': message,
                    'status': '-1'
                }
                return JsonResponse(data = resp, status=200)
        except Exception as e:
            return JsonResponse(data = {
                            "message": str(e),
                            'status': '-1'
                        }, status=400)