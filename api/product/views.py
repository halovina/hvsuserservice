import csv
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from product.views import (checkProduct, getListProduct, createProduct, 
                           updateProduct, deleteProduct, product_bulk_insert,
                           filterDataProductByDate, generateTokenDownloadCSV, checkExpiredTime)
from api.serializers import ProductSerializer, FilterDataProduct
from django.utils.decorators import method_decorator
from api.decorators import auth_user_token
from internal.pyjwt import jwtDecode
from django.http import HttpResponse

common_response = {
    "message":"Service Request Success",
    "status":"00"
}
class ProductView(APIView):
    @method_decorator(auth_user_token)
    def get(self, *args, **kwargs):
        try:
            lst = getListProduct()
            common_response["data"] = lst
            return JsonResponse(data = common_response, status=200)
        except Exception as e:
            common_response["message"] = str(e)
            common_response["status"] = "-1"
        return JsonResponse(common_response, status=400)
    
    @method_decorator(auth_user_token)
    def post(self, *args, **kwargs):
        try:
            data = JSONParser().parse(self.request)
            serializer = ProductSerializer(data=data, many=True)
            if serializer.is_valid():
                message, status = product_bulk_insert(data)
                common_response["message"] = message
                common_response["status"] = status
                common_response["data"] = data
                return JsonResponse(data = common_response, status=200)
            else:
                common_response["message"] = serializer.errors
                common_response["status"] = "-1"
                return JsonResponse(common_response, status=400)
        except Exception as e:
            common_response["message"] = str(e)
            common_response["status"] = "-1"
        return JsonResponse(common_response, status=400)
    
    @method_decorator(auth_user_token)    
    def put(self, request, key, *args, **kwargs):
        try:
            data = JSONParser().parse(self.request)
            serializer = ProductSerializer(data=data)
            if serializer.is_valid():
                message, status = updateProduct(key, data)
                common_response["message"] = message
                common_response["status"] = status
                data['id'] = key
                common_response["data"] = data
                return JsonResponse(data = common_response, status=200)
            else:
                common_response["message"] = serializer.errors
                common_response["status"] = "-1"
                return JsonResponse(common_response, status=400)
        except Exception as e:
            common_response["message"] = str(e)
            common_response["status"] = "-1"
        return common_response
    
    @method_decorator(auth_user_token)
    def delete(self, request, key, *args, **kwargs):
        try:
            message, status = deleteProduct(key)
            common_response["message"] = message
            common_response["status"] = status
            return JsonResponse(data = common_response, status=200)
        except Exception as e:
            common_response["message"] = str(e)
            common_response["status"] = "-1"
        return common_response
    
    
class FilterProductView(APIView):
    @method_decorator(auth_user_token)
    def post(self, *args, **kwargs):
        try:
            data = JSONParser().parse(self.request)
            serializer = FilterDataProduct(data=data)
            if serializer.is_valid():
                list_data, message = filterDataProductByDate(data)
                if len(list_data) > 0:
                    download_url = "http://localhost:8000/api/v1/product/download-csv/{}".format(generateTokenDownloadCSV(data))
                else:
                    download_url = ""
                common_response["message"] = message
                common_response["status"] = '00'
                common_response["data"] = {
                    "start_date":data['date_from'],
                    "end_date":data['date_end'],
                    "total": len(list_data),
                    "download_url": download_url
                }
                return JsonResponse(data = common_response, status=200)
            else:
                common_response["message"] = serializer.errors
                common_response["status"] = "-1"
                return JsonResponse(common_response, status=400)
        except Exception as e:
            common_response["message"] = str(e)
            common_response["status"] = "-1"
        return JsonResponse(common_response, status=400)
    
class DownloadFileCsvProduct(APIView):
    def get(self, request, key, *args, **kwargs):
        try:
            resp = jwtDecode(key)
            validate = checkExpiredTime(resp['expired_time'])
            if validate:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="{}-listproduct.csv"'.format(datetime.now().timestamp())
                writer = csv.writer(response,delimiter=';')
                writer.writerow([
                    'Name',
                    'Price',
                    'Status',
                    'CreatedDate'
                ])
                wml = filterDataProductByDate({
                    'date_from': resp['date_from'],
                    'date_end': resp['date_end']
                })
                for wr in wml:
                    row = [
                        wr.name,
                        wr.price,
                        wr.status,
                        wr.created_date.strftime("%Y-%m-%d %H:%M:%S")
                    ]
                    writer.writerow(row)
                return response
            else:
                return JsonResponse(data = {
                                "message": "link download expired"
                            }, status=200)
        except Exception as e:
            return JsonResponse(data = {
                            "message": str(e)
                        }, status=400)
        