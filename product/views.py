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
        data['name'] = vprd.name
        data['price'] = vprd.price
        data['status'] = vprd.status
        lst.append(data)
    connection.close()
    return lst

def createProduct(data):
    try:
        product = Product(
            name = data['name'],
            price = data['price'],
            status = data['status']
        )
        product.save()
        connection.close()
        
        response_status_code = "00"
        message = "Create product success"
    except Exception as e:
        response_status_code = "-1"
        message = str(e)
    return response_status_code, message
    
def updateProduct(productId, data):
    try:
        product = Product.obejcts.get(id=productId)
        product.name = data['name'],
        product.price = data['price'],
        product.status = data['status']
        product.save()
        connection.close()
        
        response_status_code = "00"
        message = "Update product success"
    except Exception as e:
        response_status_code = "-1"
        message = str(e)
    return response_status_code, message
    
def deleteProduct(productId):
    try:
        Product.objects.filter(id=productId).delete()
        response_status_code = "00"
        message = "Delete product success"
    except Exception as e:
        response_status_code = "-1"
        message = str(e)
    return response_status_code, message
