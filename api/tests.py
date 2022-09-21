

from wsgiref import headers
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from django.contrib.auth.models import User

def createMockUser():
    User.objects.create_user(username= "admin@example.com",
                                    email="admin@example.com",
                                    password="testXyz123",
                                    is_active=True
                        )
def getAuthToken(self,payload):
    response = self.client.post("/api/v1/users/login", data=payload, format='json')
    return response

class AccountTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def test_success_login(self):
        createMockUser()
        payload = {
            "email":"admin@example.com",
            "password":"testXyz123"
        }
        response = getAuthToken(self,payload)
        self.assertEqual(response.status_code, 200)
        
    def test_failed_login(self):
        payload = {
            "email":"admin@example.com",
            "password":"testXyz123"
        }
        url = reverse('api_users_login')
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, 400)
        
class ProductTest(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]
    
    def test_success_get_list_product(self):
        createMockUser()
        payload = {
            "email":"admin@example.com",
            "password":"testXyz123"
        }
        rsp = getAuthToken(self,payload).json()
        url_prod = reverse('api_post_list_product')
        response = self.client.get(url_prod, **{ "HTTP_AUTHORIZATION": "{}".format(rsp['token']) })
        self.assertEqual(response.status_code, 200)
        