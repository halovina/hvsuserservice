from django.test import TestCase
from users.views import create_register_user

# Create your tests here.
class CreateNewUserTestCase(TestCase):
    data = {
        "email":"user@example.com",
        "password":"password@1223G",
        "full_name":"Test By Johan"
    }
    def test_create_register_user_success(self):
        resp = create_register_user(self.data)
        self.assertEqual(resp['status'], "00")