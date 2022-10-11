

import re
from wsgiref import headers
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from django.contrib.auth.models import User
from datetime import date

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
        
    def test_succes_register_new_user(self):
        payload = {
            "email":"user@example.com",
            "password":"password@1223G",
            "full_name":"Test By Johan"
        }
        url = reverse('api_users_register')
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, 200)
        
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
        
    def test_bulk_insert_success(self):
        createMockUser()
        payload_login = {
            "email":"admin@example.com",
            "password":"testXyz123"
        }
        rsp = getAuthToken(self,payload_login).json()
        
        payload_create_product = [
            {
                "name":"product bulk 1",
                "price": 1000,
                "status": "PENDING"
            },
            {
                "name":"product bulk 2",
                "price": 2000,
                "status": "PUBLISH"
            }
        ]
        response = self.client.post("/api/v1/product/",data=payload_create_product, format='json', **{ "HTTP_AUTHORIZATION": "{}".format(rsp['token']) })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'][0]['name'], 'product bulk 1')
        
        
class FilterDownloadCSVTests(APITestCase):
    def test_filter_product_by_date_success(self):
        createMockUser()
        payload_login = {
            "email":"admin@example.com",
            "password":"testXyz123"
        }
        rsp = getAuthToken(self,payload_login).json()
        
        payload_create_product = [
            {
                "name":"product bulk 1",
                "price": 1000,
                "status": "PENDING"
            },
            {
                "name":"product bulk 2",
                "price": 2000,
                "status": "PUBLISH"
            }
        ]
        self.client.post("/api/v1/product/",data=payload_create_product, format='json', **{ "HTTP_AUTHORIZATION": "{}".format(rsp['token']) })
        
        payload_filter_data = {
            'date_from': date.today(),
            'date_end': ''
        }
        response = self.client.post("/api/v1/product/filter/bydate",data=payload_filter_data, format='json', **{ "HTTP_AUTHORIZATION": "{}".format(rsp['token']) })
       
        self.assertEqual(response.json()['status'], '00')
        self.assertEqual(response.json()['data']['total'], 2)
    