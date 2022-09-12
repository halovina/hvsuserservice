from calendar import c
from django.shortcuts import render
from product.models import Product
from django.db import connection

# Create your views here.
def checkProduct(productId):
    checkData = Product.objects.filter(id=productId)
    if len(checkData) > 0:
        return True
    return False

def getListProduct():
    lst = []
    prd = Product.objects.all()
    for vprd in prd:
        data = {}
        data['id'] = vprd.id
        data['name'] = vprd.name
        data['price'] = vprd.price
        data['status'] = vprd.status
        lst.append(data)
    connection.close()
    return lst

def createProduct(data):
    productId = None
    try:
        product = Product(
            name = data['name'],
            price = data['price'],
            status = data['status']
        )
        product.save()
        
        response_status_code = "00"
        message = "Create product ({}) success".format(data['name'])
        productId = product.id
    except Exception as e:
        response_status_code = "-1"
        message = str(e)
    return response_status_code, message, productId
    
def updateProduct(productId, data):
    try:
        product = Product.objects.get(id=productId)
        product.name = data['name']
        product.price = data['price']
        product.status = data['status']
        product.save()
        
        response_status_code = "00"
        message = "Update product ({}) success".format(data['name'])
    except Exception as e:
        response_status_code = "-1"
        message = str(e)
    return response_status_code, message
    
def deleteProduct(productId):
    try:
        prd = Product.objects.filter(id=productId)
        if len(prd) > 0:
            prd.delete()
            response_status_code = "00"
            message = "Delete product ({}) success".format(productId)
        else:
            response_status_code = "-1"
            message = "Data productId ({}) tidak ditemukan".format(productId)
    except Exception as e:
        response_status_code = "-1"
        message = str(e)
    return response_status_code, message
