from django.urls import path
from api.users.views import LoginView

urlpatterns = [
    path('v1/users/login', LoginView.as_view(), name='api_users_login')
]
