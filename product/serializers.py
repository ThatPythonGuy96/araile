from .models import *
from rest_framework import serializers

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'product']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category', 'slug']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['subcategory', 'category', 'slug']    

class SubSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Sub_SubCategory
        fields = ['sub_subcategory', 'subcategory', 'slug']

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['product', 'key', 'value']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    sub_subcategory = SubSubCategorySerializer(read_only=True)
    specification = SpecificationSerializer(many=True, read_only=True)
    product_images = serializers.SerializerMethodField()
    specification = serializers.SerializerMethodField()

    def get_specification(self, obj):
        specifications = obj.specifications.all()
        return SpecificationSerializer(specifications, many=True).data

    def get_product_images(self, obj):
        images = obj.images.all()
        return ProductImageSerializer(images, many=True).data

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'brand', 'color', 'sku', 
                    'category', 'subcategory', 'sub_subcategory', 'stock', 'size', 'visibility', 
                    'warranty', 'slug', 'product_images', 'specification'
                ]

class CreateProductSerializer(serializers.ModelSerializer):
    product_images = serializers.ListField(child=serializers.ImageField())
    specification = serializers.DictField(required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())
    sub_subcategory = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'brand', 'color', 'sku', 
                    'category', 'subcategory', 'sub_subcategory', 'stock', 'size', 'visibility', 
                    'warranty', 'product_images', 'specification'
                ]
        
    def create(self, validated_data):
        images_data = validated_data.pop('product_images', [])
        specifications_data = validated_data.pop('specification', [])
        product = Product.objects.create(**validated_data)
        
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        
        for specification_data in specifications_data:
            Specification.objects.create(product=product, **specification_data)
        
        return product
