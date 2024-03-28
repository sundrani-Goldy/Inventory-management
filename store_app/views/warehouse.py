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
    
    def create_warehouse_inventory_from_product(product_instance, user):
        warehouses = Warehouse.objects.all()
        for warehouse in warehouses:
            warehouse_inventory = WarehouseInventory.objects.create(
                fk_product=product_instance,
                fk_warehouse=warehouse,
                updated_by=user,  
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

    def create_warehouse_inventory_from_warehouse(warehouse_instance,user):
        products = Product.objects.all()
        for product in products:
            warehouse_inventory=WarehouseInventory.objects.create(
                fk_product=product,
                fk_warehouse=warehouse_instance,
                updated_by=user,  
                available_quantity=0,
                allotted_quantity=0,
                total_quantity=0,
                sold_quantity=0,
                product_total_valuation=0,
                on_hand=0,
            )
            for tag in warehouse_instance.fk_tag.all():
                warehouse_inventory.fk_tag.add(tag)
    


    def partial_update(self, request, *args, **kwargs):
        warehouse_inventory_id = kwargs['pk']
        warehouse_inventory = WarehouseInventory.objects.get(id=warehouse_inventory_id)
        reason = request.data.get('reason')

        if not reason:
            return Response('Reason is Required', status=status.HTTP_400_BAD_REQUEST)

        fk_tag_d = request.data.get("fk_tag", [tag.id for tag in warehouse_inventory.fk_tag.all()]) 
        print(fk_tag_d, 'inside partial update before setting')
        old_quantity = warehouse_inventory.available_quantity
        warehouse_inventory.available_quantity = request.data.get('available_quantity', warehouse_inventory.available_quantity)
        warehouse_inventory.allotted_quantity = request.data.get('allotted_quantity', warehouse_inventory.allotted_quantity)
        warehouse_inventory.total_quantity = request.data.get('total_quantity', warehouse_inventory.total_quantity)
        warehouse_inventory.sold_quantity = request.data.get('sold_quantity', warehouse_inventory.sold_quantity)
        warehouse_inventory.damage_quantity = request.data.get('damage_quantity', warehouse_inventory.damage_quantity)
        warehouse_inventory.fk_tag.set(fk_tag_d)
        warehouse_inventory.product_total_valuation = warehouse_inventory.fk_product.mrp * warehouse_inventory.available_quantity
        warehouse_inventory.on_hand = request.data.get('available_quantity', warehouse_inventory.available_quantity) + request.data.get('damage_quantity', warehouse_inventory.damage_quantity)
        serializer = WarehouseInventorySerializer(warehouse_inventory, data=request.data, partial=True)

        if serializer.is_valid():
            a = serializer.save()
            # print(fk_tag_d, 'inside partial update before saving')
            # Signal to create InventoryLog
            create_inventory_log(a , old_quantity,reason)
            create_or_update_inventory(a)
            return Response(serializer.data)

        return Response(serializer.errors)

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        pass