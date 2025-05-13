from .models import *
from rest_framework import serializers

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'product']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category', 'slug']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory', 'category', 'slug']    

class SubSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Sub_SubCategory
        fields = ['id', 'sub_subcategory', 'subcategory', 'slug']

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['id', 'product', 'key', 'value']

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
        fields = ['id', 'name', 'description', 'price', 'brand', 'color', 'sku', 
                    'category', 'subcategory', 'sub_subcategory', 'stock', 'size', 'visibility', 
                    'warranty', 'slug', 'product_images', 'specification'
                ]

from rest_framework import serializers
from .models import Product, ProductImage, Specification, Category, SubCategory, Sub_SubCategory

class CreateProductSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), 
        write_only=True,
        required=True
    )
    specifications = serializers.DictField(write_only=True, required=False)
    category = serializers.IntegerField(write_only=True)
    subcategory = serializers.IntegerField(write_only=True)
    sub_subcategory = serializers.IntegerField(write_only=True)

    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'brand', 'color', 'sku',
            'category', 'subcategory', 'sub_subcategory',
            'stock', 'size', 'visibility', 'warranty',
            'images', 'specifications'
        ]

    def create(self, validated_data):
        # Extract nested fields
        images = validated_data.pop('images', [])
        specifications = validated_data.pop('specifications', {})

        category_id = validated_data.pop('category')
        subcategory_id = validated_data.pop('subcategory')
        sub_subcategory_id = validated_data.pop('sub_subcategory')

        # Retrieve related model instances
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError({'category': 'Invalid category ID.'})
        
        try:
            subcategory = SubCategory.objects.get(pk=subcategory_id)
        except SubCategory.DoesNotExist:
            raise serializers.ValidationError({'subcategory': 'Invalid subcategory ID.'})
        
        try:
            sub_subcategory = Sub_SubCategory.objects.get(pk=sub_subcategory_id)
        except Sub_SubCategory.DoesNotExist:
            raise serializers.ValidationError({'sub_subcategory': 'Invalid sub-subcategory ID.'})

        # Create the product
        product = Product.objects.create(
            category=category,
            subcategory=subcategory,
            sub_subcategory=sub_subcategory,
            **validated_data
        )

        # Save images
        for image in images:
            ProductImage.objects.create(product=product, image=image)

        # Save specifications (key-value pairs)
        for key, value in specifications.items():
            Specification.objects.create(product=product, key=key, value=value)

        return product
