from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from product.views import checkProduct, getListProduct, createProduct, updateProduct, deleteProduct
from api.serializers import ProductSerializer
from django.utils.decorators import method_decorator
from api.decorators import auth_user_token

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
    
    def post(self, *args, **kwargs):
        try:
            data = JSONParser().parse(self.request)
            serializer = ProductSerializer(data=data)
            if serializer.is_valid():
                message, status, productId = createProduct(data)
                common_response["message"] = message
                common_response["status"] = status
                data['id'] = productId
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