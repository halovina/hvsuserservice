from urllib import response
from django.test import TestCase
from product.models import Product
from product.views import createProduct

# Create your tests here.
class ModelsTestCase(TestCase):
    def test_create_product(self):
        product = Product.objects.create(
            name = 'test 1',
            price = 1000,
            status = 'PENDING'
        )
        self.assertEqual(product.name, "test 1")
        self.assertEqual(product.price, 1000)
        self.assertEqual(product.status, 'PENDING')
        
    def test_error_create_product(self):
        with self.assertRaises(ValueError):
            Product.objects.create(
            name = 'test 1',
            price = "test string",
            status = 'PENDING'
        )
        
        
    
class ViewsTestCase(TestCase):
    def test_sucess_createProduct(self):
        data = {
            "name" : "test 1",
            "price": "1000",
            "status" : "PENDING"
        }
        response_status_code, message, _ = createProduct(data)
        self.assertEqual(response_status_code, "00")
        self.assertEqual(message, "Create product ({}) success".format(data['name']))
        
    def test_exception_createProduct(self):
        data = {
            "name" : "test 1",
            "price": "test string",
            "status" : "PENDING"
        }
        response_status_code, message, _ = createProduct(data)
        self.assertRaisesMessage(Exception, message)
        self.assertEqual(response_status_code, "-1")