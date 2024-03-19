from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework import status
from drf_yasg import openapi
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from store_app.serializers.order import *
from store_app.models.order import *



class OrderView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     order_details = OrderDetailSerializer(data=data, many=True)
    #     if order_details.is_valid():
    #         fk_order_detail = order_details.save()
    #         data['fk_order_detail'] = fk_order_detail
    #         order = OrderSerializer(data=data)
    #         if order.is_valid():
    #             order.save()
    #             return Response(order.data, status=status.HTTP_201_CREATED)
    #         else:
    #             return Response(order.errors, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response(order_details.errors, status=status.HTTP_400_BAD_REQUEST)