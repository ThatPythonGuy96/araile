from rest_framework import serializers
from .models import *
from product.models import Product

class CreateOrderSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ['product']

    def create(self, validated_data):
        account = self.context['request'].user
        product_id = validated_data['product']
        product_obj = Product.objects.get(id=product_id)

        order = Order.objects.create(
            customer=account,
            product=product_obj
        )
        order.save()
        return order

class OrderSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')
    customer = serializers.CharField(source='customer.email')

    class Meta:
        model = Order
        fields = ['order_id', 'customer', 'product', 'status', 'total', 'order_date']
        read_only_fields = ['order_id', 'order_date']