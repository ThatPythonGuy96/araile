from .models import *
from . import serializers
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Product"])
class ProductsView(APIView):
    # permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.ProductSerializer

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@extend_schema(tags=["Product"])
class CreateProductView(APIView):
    # permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.CreateProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = serializers.CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)