from telnetlib import STATUS
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
   email = serializers.CharField(max_length=50)
   password = serializers.CharField(max_length=50)
   
class ProductSerializer(serializers.Serializer):
   name = serializers.CharField(max_length=150)
   price = serializers.IntegerField()
   status = serializers.CharField(allow_blank=True)