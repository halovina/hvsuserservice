from django.contrib.auth import authenticate
from django.contrib.auth.models import User

common_response = {
    "status":"",
    "message":""
}

def checkUserLogin(email, password):
    user = authenticate(username=email, password=password)
    if user is not None:
        return True
    else:
        return False
    
def create_register_user(data):
    try:
        User.objects.create_user(username= data['email'],
                                    email=data['email'],
                                    password=data['password'],
                                    first_name=data['full_name']
                        )
        common_response['status'] = '00'
        common_response['message'] = 'Register Success, Check email and click link activation'
    except Exception as e:
        common_response['status'] = '-1'
        common_response['message'] = str(e)
    return common_response
    