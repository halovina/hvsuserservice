import jwt
from django.conf import settings

def jwtEncode(payload):
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return jwt_token

def jwtDecode(jwt_token):
    payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms="HS256")
    return payload