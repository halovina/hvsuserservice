from calendar import c
from email import message
from unicodedata import name
from django.shortcuts import render
from product.models import Product
from django.db import connection
from django.utils import timezone
from datetime import datetime
from internal.pyjwt import jwtEncode


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



def product_bulk_insert(data):
    try:
        instance_transaction = [
            Product(
                name = x['name'],
                price = x['price'],
                status = x['status']
            )
            for x in data
        ]
        Product.objects.bulk_create(instance_transaction)
        response_status_code = "00"
        message = "Create product ({} list data) success".format(len(data))
    except Exception as e:
        response_status_code = "-1"
        message = str(e)
    return response_status_code, message


def filterDataProductByDate(data):
    try:
        date_from = "{} 00:00:00".format(data['date_from']) #2022-09-01 00:00:00
        if data['date_end'] == "":
            date_end = "{} 23:59:00".format(data['date_from']) #2022-09-02 23:59:00
        else:
            date_end = "{} 23:59:00".format(data['date_end'])
            
        f_aware = timezone.make_aware(datetime.strptime(date_from,"%Y-%m-%d %H:%M:%S"), timezone.get_current_timezone())
        t_aware = timezone.make_aware(datetime.strptime(date_end,"%Y-%m-%d %H:%M:%S"), timezone.get_current_timezone())
        
        getProduct = Product.objects.filter(created_date__range=(f_aware, t_aware))
        lst = []
        for prd in getProduct:
            lst_prd = {}
            lst_prd['name'] = prd.name
            lst_prd['price'] = prd.price
            lst_prd['status'] = prd.status
            lst_prd['created'] = prd.created_date
            lst.append(lst_prd)
        return lst, "Get list data product success"
        
    except Exception as e:
        return [], str(e)
    
def generateTokenDownloadCSV(data):
    curent_time = datetime.now()
    curent_unix_time = curent_time.timestamp()
    expired_time = curent_unix_time + (5 * 60)
    payload = {
        'date_from': data['date_from'],
        'date_end': data['date_end'],
        'expired_time': int(expired_time)
    }
    token = jwtEncode(payload)
    return token

def checkExpiredTime(expired_time):
    curent_time = datetime.now()
    curent_unix_time = curent_time.timestamp()
    if int(curent_unix_time) < expired_time:
        return True
    else:
        return False
