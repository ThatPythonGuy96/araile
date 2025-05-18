from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from . import models, serializers
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Order"])
class CreateOrderView(APIView):
    serializer_class = serializers.CreateOrderSerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = serializers.CreateOrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'success': 'Order has been placed.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Order"])
class OrdersView(APIView):
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        orders = models.Order.objects.all().order_by('-order_date')
        serializer = serializers.OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)