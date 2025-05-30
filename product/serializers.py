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
        fields = ['specification', 'type', 'value']
    
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    sub_subcategory = SubSubCategorySerializer(read_only=True)
    specification = SpecificationSerializer(many=True, read_only=True)
    product_images = serializers.SerializerMethodField()
    specification = serializers.SerializerMethodField()

    def get_specification(self, obj):
        if obj.specifications:
            specifications = obj.specifications.all()
            return SpecificationSerializer(specifications, many=True).data

    # @extend_schema_field(field=str)
    def get_product_images(self, obj):
        images = obj.images.all()
        return ProductImageSerializer(images, many=True).data

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'brand', 'color', 'sku', 
                    'category', 'subcategory', 'sub_subcategory', 'stock', 'size', 'visibility', 
                    'warranty', 'slug', 'product_images', 'specification'
                ]

class CreateProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    brand = serializers.CharField()
    category = serializers.IntegerField(write_only=True)
    subcategory = serializers.IntegerField(write_only=True)
    sub_subcategory = serializers.IntegerField(write_only=True)
    color = serializers.CharField()
    sku = serializers.CharField()
    stock = serializers.IntegerField() 
    size = serializers.IntegerField()
    visibility = serializers.BooleanField()
    warranty = serializers.IntegerField()
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)
    specifications = SpecificationSerializer(write_only=True, many=True)
    # specification_type = serializers.CharField()
    # specification_value = serializers.CharField()
    
    class Meta:
        model = Product
        fields = (
            'name', 'description', 'price', 'brand', 'color', 'sku', 'category', 'subcategory', 'sub_subcategory',
            'stock', 'size', 'visibility', 'warranty', 'images', 'specifications'
        )

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        category_id = validated_data.pop('category')
        subcategory_id = validated_data.pop('subcategory')
        sub_subcategory_id = validated_data.pop('sub_subcategory')

        try:
            category = Category.objects.get_or_create(id=category_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError({'category': 'Invalid category ID.'})
        
        try:
            subcategory = SubCategory.objects.get_or_create(id=subcategory_id, category=category)
        except SubCategory.DoesNotExist:
            raise serializers.ValidationError({'subcategory': 'Invalid subcategory ID.'})
        
        try:
            sub_subcategory = Sub_SubCategory.objects.get_or_create(id=sub_subcategory_id, subcategory=subcategory)
        except Sub_SubCategory.DoesNotExist:
            raise serializers.ValidationError({'sub_subcategory': 'Invalid sub-subcategory ID.'})

        product = Product.objects.create(
            category=category,
            subcategory=subcategory,
            sub_subcategory=sub_subcategory,
            **validated_data
        )

        for image in images:
            ProductImage.objects.create(product=product, image=image)

        Specification.objects.create(
            product=product,
            specification=validated_data['specification'],
            type=validated_data['specification_type'],
            value=validated_data['specification_value']
        )

        return product
    
class ProductUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_null=True, required=False)
    description = serializers.CharField(allow_null=True, required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True, required=False)
    brand = serializers.CharField(allow_null=True, required=False)
    category = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    subcategory = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    sub_subcategory = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    color = serializers.CharField(allow_null=True, required=False)
    sku = serializers.CharField(allow_null=True, required=False)
    stock = serializers.IntegerField(allow_null=True, required=False) 
    size = serializers.IntegerField(allow_null=True, required=False)
    visibility = serializers.BooleanField(allow_null=True, required=False)
    warranty = serializers.IntegerField(allow_null=True, required=False)
    images = serializers.ListField(child=serializers.ImageField(), allow_null=True, required=False)
    specifications = SpecificationSerializer(write_only=True, many=True, allow_null=True, required=False)


    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'brand', 'color', 'sku', 'category', 'subcategory', 'sub_subcategory',
            'stock', 'size', 'visibility', 'warranty', 'images', 'specifications')

    def validate(self, data):
        request = self.context.get('request')
        data["images_sent"] = "images" in request.data
        return data

    def update(self, instance, validated_data):
        images_sent = validated_data.pop("images_sent", False)
        category_id = validated_data.pop("category", None)
        subcategory_id = validated_data.pop('subcategory', None)
        sub_subcategory_id = validated_data.pop('sub_subcategory', None)
        specs_data = validated_data.pop("specifications", None)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.brand = validated_data.get("brand", instance.brand)
        instance.color = validated_data.get("color", instance.color)
        instance.sku = validated_data.get("sku", instance.sku)
        instance.stock = validated_data.get("stock", instance.stock)
        instance.size = validated_data.get("size", instance.size)
        instance.visibility = validated_data.get("visibility", instance.visibility)
        instance.warranty = validated_data.get("warranty", instance.warranty)

        new_name = validated_data.get('name')
        if new_name and new_name != instance.name:
            instance.name = new_name

        if category_id:
            instance.category = Category.objects.get(id=category_id)

        if subcategory_id:
            instance.subcategory = SubCategory.objects.get(id=subcategory_id)

        if sub_subcategory_id:
            instance.sub_subcategory = Sub_SubCategory.objects.get(id=sub_subcategory_id)

        if images_sent:
            new_images = validated_data.get('images', [])
            instance.images.all().delete()
            for image in new_images:
                ProductImage.objects.create(product=instance, image=image)

        if specs_data is not None:
            instance.specifications.all().delete()
            for spec in specs_data:
                Specification.objects.create(product=instance, **spec)

        instance.save()
        return instance