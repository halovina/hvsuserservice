from datetime import datetime
from rest_framework.views import APIView
from api.serializers import LoginSerializer
from rest_framework.parsers import JSONParser
from users.views import checkUserLogin
from django.http import JsonResponse
from api.pyjwt import jwtEncode
from django.utils import timezone

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