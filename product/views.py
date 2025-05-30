from .models import *
from . import serializers
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Product"])
class ProductsView(APIView):
    serializer_class = serializers.ProductSerializer

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=["Product"])
class ProductView(APIView):
    serializer_class = serializers.ProductSerializer

    def get(self, request, id):
        product = Product.objects.get(id=id)
        serializer = serializers.ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@extend_schema(tags=["Product"])
class CreateProductView(APIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.CreateProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = serializers.CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Product"])     
class ProductUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.ProductUpdateSerializer

    def patch(self, request, id):
        try:
            product = Product.objects.get(id=id)
            if request.user.is_admin:
                serializer = serializers.ProductUpdateSerializer(product, data=request.data, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error:", "You don't have permission to perform this operation."}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error:", str(e)}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Product"])     
class ProductDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
            if request.user.is_admin:
                product.delete()
                return Response({"success": "Product Deleted"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error:", "You don't have permission to perform this operation."}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error:", str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
    
@extend_schema(tags=["Product"])
class CategoryView(APIView):
    serializer_class = serializers.CategorySerializer

    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        serializer = serializers.CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@extend_schema(tags=["Product"])
class SubCategoryView(APIView):
    serializer_class = serializers.SubCategorySerializer

    def get(self, request, slug, category):
        subcategory = SubCategory.objects.get(slug=slug, category=category)
        serializer = serializers.SubCategorySerializer(subcategory)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=["Product"])
class Sub_SubCategoryView(APIView):
    serializer_class = serializers.SubSubCategorySerializer

    def get(self, request, slug, subcategory):
        sub_subcategory = Sub_SubCategory.objects.get(slug=slug, subcategory=subcategory)
        serializer = serializers.SubSubCategorySerializer(sub_subcategory)
        return Response(serializer.data, status=status.HTTP_200_OK)
