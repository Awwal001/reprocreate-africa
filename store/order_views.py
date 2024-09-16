from store.models import Product, Order, OrderProduct, ShippingAddress
from store.serializers import ProductSerializer, OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class OrderCreateView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Log or print the errors for debugging
            print("Validation Errors: ", serializer.errors)  # This will help debug validation issues
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      


class OrderDetailView(APIView):
    def get(self, request, tracking_number):
        # Fetch the order by tracking number
        order = get_object_or_404(Order, tracking_number=tracking_number)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, tracking_number):
        # Fetch the order by tracking number
        order = get_object_or_404(Order, tracking_number=tracking_number)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, tracking_number):
        # Fetch the order by tracking number
        order = get_object_or_404(Order, tracking_number=tracking_number)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class OrderListView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
