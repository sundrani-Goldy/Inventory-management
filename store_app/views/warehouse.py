from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import logging
import os
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.http import HttpResponseServerError
from rest_framework import status
from store_app.serializers.warehouse import WarehouseSerializer,WarehouseInventorySerializer
from store_app.models.inventory_and_warehouse.warehouse import Warehouse,WarehouseInventory,OtherDetail
from store_app.models.product import Product
from store_app.models.inventory_and_warehouse.warehouse import Warehouse
from django.db.models.signals import post_save
from store_app.views.inventory import create_inventory_log,create_or_update_inventory

from store_app.models.product_detail import Tag
from store_app.serializers.inventory import InventorySerializer,InventoryLogSerializer
from store_app.models.inventory_and_warehouse.inventory import Inventory,InventoryLog
from django.db.models.signals import post_save
from store_app.views.inventory import create_inventory_log,create_or_update_inventory

class WarehouseView(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    queryset = Warehouse.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        data['fk_user'] = user.id
        warehouse_serializer = WarehouseSerializer(data=data)
        
        
        if warehouse_serializer.is_valid():
            # Assign the authenticated user to fk_user during warehouse creation
            warehouse = warehouse_serializer.save()
            WarehouseInventoryView.create_warehouse_inventory_from_warehouse(warehouse, user)
            return Response(warehouse_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(warehouse_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Check if there's only one warehouse left
        if Warehouse.objects.count() == 1:
            return Response({"Cannot delete the only remaining warehouse."}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
        return Response( "Warehouse Deleted Successfully",status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        pass



class WarehouseInventoryView(ModelViewSet):
    serializer_class = WarehouseInventorySerializer
    queryset = WarehouseInventory.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

class OtherDetailView(viewsets.ModelViewSet):
    queryset = OtherDetail.objects.all()
    serializer_class = OtherDetailSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]
    