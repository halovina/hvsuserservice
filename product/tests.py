from urllib import response
from django.test import TestCase
from product.models import Product
from product.views import createProduct, filterDataProductByDate
from datetime import date

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
    compose_data = {
            "name" : "test 1",
            "price": "1000",
            "status" : "PENDING"
        }
    def test_sucess_createProduct(self):
        response_status_code, message, _ = createProduct(self.compose_data)
        self.assertEqual(response_status_code, "00")
        self.assertEqual(message, "Create product ({}) success".format(self.compose_data['name']))
        
    def test_exception_createProduct(self):
        failed_compose_data = {
            "name" : "test 1",
            "price": "testtt",
            "status" : "PENDING"
        }
        response_status_code, message, _ = createProduct(failed_compose_data)
        self.assertRaisesMessage(Exception, message)
        self.assertEqual(response_status_code, "-1")
        
    def test_filterDataProductByDate_with_data(self):
        createProduct(self.compose_data)
        filter_data = {
            'date_from': date.today(),
            'date_end': ''
        }
        resp, message = filterDataProductByDate(filter_data)
        self.assertEqual(message, "Get list data product success")
        