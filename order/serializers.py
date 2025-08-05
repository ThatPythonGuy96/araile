from rest_framework import serializers
from .models import *
from product.models import Product, ProductImage

class CustomDateTimeSerializer(serializers.DateTimeField):
    def to_representation(self, value):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    
class AddToOrderSerializer(serializers.Serializer):
   quantity = serializers.IntegerField()
   product_id = serializers.IntegerField()

class OrderProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'product']

class OrderProductSerializer(serializers.ModelSerializer):
    product_images = serializers.SerializerMethodField()

    # @extend_schema_field(field=str)
    def get_product_images(self, obj):
        images = obj.images.all()
        return OrderProductImageSerializer(images, many=True).data

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'product_images']
        
class OrderItemSerializer(serializers.ModelSerializer):
    item_total = serializers.SerializerMethodField()
    product = OrderProductSerializer(read_only=True)
        
    def get_item_total(self, obj):
        price = obj.product.price * obj.quantity
        return f"{price:,.2f}"

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'item_total')

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.email')
    order_date = CustomDateTimeSerializer()
    updated = CustomDateTimeSerializer()
    items = OrderItemSerializer(read_only=True, many=True)
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        total_price = sum([(item.product.price) * item.quantity for item in obj.items.all()])
        return f"{total_price:,.2f}"

    class Meta:
        model = Order
        fields = ('order_id', 'customer', 'items', 'status', 'order_date', 'updated', 'total')
        read_only_fields = ['order_id', 'order_date', 'updated']