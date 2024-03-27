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
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.http import HttpResponseServerError
from rest_framework import status
from store_app.serializers.warehouse import WarehouseSerializer,WarehouseInventorySerializer
from store_app.models.inventory_and_warehouse.warehouse import Warehouse,WarehouseInventory,OtherDetail
from store_app.models.product import Product
from store_app.models.inventory_and_warehouse.warehouse import Warehouse
from store_app.models.product_detail import Tag
from store_app.serializers.inventory import InventorySerializer,InventoryLogSerializer
from store_app.models.inventory_and_warehouse.inventory import Inventory,InventoryLog
from rest_framework.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

class WarehouseView(ModelViewSet):
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
    
    # @staticmethod
    def create_warehouse_inventory_from_product(product_instance, user):
        warehouses = Warehouse.objects.all()
        for warehouse in warehouses:
            warehouse_inventory = WarehouseInventory.objects.create(
                fk_product=product_instance,
                fk_warehouse=warehouse,
                updated_by=user,  # Pass the user object here
                available_quantity=0,
                allotted_quantity=0,
                total_quantity=0,
                sold_quantity=0,
                product_total_valuation=0,
                on_hand=0,
            )
            # Adding related tags to WarehouseInventory
            for tag in product_instance.fk_tag.all():
                warehouse_inventory.fk_tag.add(tag)

    # @staticmethod
    def create_warehouse_inventory_from_warehouse(warehouse_instance,user):
        products = Product.objects.all()
        for product in products:
            warehouse_inventory=WarehouseInventory.objects.create(
                fk_product=product,
                fk_warehouse=warehouse_instance,
                updated_by=user,  # Assuming the user who created the warehouse is updating
                available_quantity=0,
                allotted_quantity=0,
                total_quantity=0,
                sold_quantity=0,
                product_total_valuation=0,
                on_hand=0,
            )
            for tag in warehouse_instance.fk_tag.all():
                warehouse_inventory.fk_tag.add(tag)
    


    
    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        pass
