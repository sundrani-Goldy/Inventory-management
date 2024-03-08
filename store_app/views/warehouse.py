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
from store_app.serializers.warehouse import *
from store_app.models.inventory_and_warehouse.warehouse import *


class WarehouseView(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAdminUser]
    authentication_class = [TokenAuthentication]


class WarehouseInventoryView(viewsets.ModelViewSet):
    queryset = WarehouseInventory.objects.all()
    serializer_class = WarehouseInventorySerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

class OtherDetailView(viewsets.ModelViewSet):
    queryset = OtherDetail.objects.all()
    serializer_class = OtherDetailSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]
    