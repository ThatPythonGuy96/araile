from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from . import models, serializers
from product.models import Product
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Order"])
class OrdersView(APIView):
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        customer = self.request.user
        if models.Order.objects.filter(customer=customer).exists():
            order = models.Order.objects.get(customer=customer, paid=False)
            serializer = serializers.OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("Order does not exist.", status=status.HTTP_200_OK)
        
@extend_schema(tags=["Order"])
class AddToOrderItem(APIView):
    serializer_class = serializers.AddToOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            product_id = request.data.get("product_id")
            quantity = request.data.get("quantity")
            user = self.request.user
            product = Product.objects.get(id=product_id)

            order, created = models.Order.objects.get_or_create(customer=user)
            orderitem, created = models.OrderItem.objects.get_or_create(order=order, product=product, quantity=quantity)
            # if orderitem:
            #     orderitem.quantity += quantity
            orderitem.save()

            serializer = serializers.OrderItemSerializer(orderitem)
            return Response({"data": serializer.data, "success": "Product added to cart."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error:", str(e)}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Order"])     
class DeleteOrderItem(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, orderitem_id):
        try:
            orderitem = models.OrderItem.objects.get(id=orderitem_id)
            orderitem.delete()
            return Response({"success": "Product Removed from cart."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error:", str(e)}, status=status.HTTP_400_BAD_REQUEST)
