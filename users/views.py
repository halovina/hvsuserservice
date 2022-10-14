from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from datetime import datetime
from internal.pyjwt import jwtEncode, jwtDecode
from django.conf import settings
from api.decorators import checkTokenExpired
from users.sendemail import forward_email

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
        link_url = generate_link_download(data)
        
        forward_email({
            'email': data['email'],
            'link_url': link_url
        })
        common_response['status'] = '00'
        common_response['message'] = 'Register Success, Check email and click link activation'
    except Exception as e:
        common_response['status'] = '-1'
        common_response['message'] = str(e)
    return common_response

def generate_link_download(data):
    curent_time = datetime.now()
    curent_unix_time = curent_time.timestamp()
    expired_time = curent_unix_time + (5 * 60)
    payload ={
        'email': data['email'],
        'datetime_now': str(datetime.now()),
        'expired_time': int(expired_time)
        
    }
    token = jwtEncode(payload)
    url = "{}/api/v1/users/link/activation/{}".format(settings.SITE_URL, token)
    return url

def validate_token_url(token):
    try:
        data = jwtDecode(token)
        if checkTokenExpired(data['expired_time']) == False:
            return False, 'Link activation expired'
        check_user = User.objects.filter(email=data['email']).exists()
        if check_user == False:
            return False, 'User not found'
    except Exception as e:
        return False, "Link activation not authorized"
    return True, 'Valid link activation'

def activate_account_user(token):
    try:
        data = jwtDecode(token)
        user = User.objects.get(email=data['email'])
        user.is_active = True
        user.save()
    except Exception as e:
        return False, str(e)
    return True, 'success'
            
    
    
    