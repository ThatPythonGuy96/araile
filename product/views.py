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

@extend_schema(tags=["Product"])
class CategoriesView(APIView):
    serializer_class = serializers.CategorySerializer

    def get(self, request):
        categories = Category.objects.all()
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=["Product"])
class SubCategoriesView(APIView):
    serializer_class = serializers.SubCategorySerializer

    def get(self, request):
        subcategories = SubCategory.objects.all()
        serializer = serializers.SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=["Product"])
class Sub_SubCategoriesView(APIView):
    serializer_class = serializers.SubSubCategorySerializer

    def get(self, request):
        sub_subcategories = Sub_SubCategory.objects.all()
        serializer = serializers.SubSubCategorySerializer(sub_subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)