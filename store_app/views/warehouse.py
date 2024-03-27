from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework import status
from drf_yasg import openapi
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
    
    def partial_update(self, request, *args, **kwargs):
        warehouse_inventory_id = kwargs['pk']
        warehouse_inventory = WarehouseInventory.objects.get(id=warehouse_inventory_id)

        # # Retrieve the most recent InventoryLog associated with the inventory
        inventory_logs = InventoryLog.objects.filter(fk_product=warehouse_inventory.fk_product).order_by('-created_at')
        
        if inventory_logs.exists():
            inventory_log = inventory_logs.first()
            reason = request.data.get("reason", inventory_log.reason)           
            damage_quantity = request.data.get("damage_quantity", inventory_log.damage_quantity)
        else:
            reason = request.data.get("reason","1st Time Created while updating warehouse inventory")
            damage_quantity = request.data.get("damage_quantity", 0)
            
        fk_tag_ids = request.data.get("fk_tag", [tag.id for tag in warehouse_inventory.fk_tag.all()]) 
        fk_product_id = request.data.get("fk_product", warehouse_inventory.fk_product.id)
        fk_warehouse_id = request.data.get("fk_warehouse", warehouse_inventory.fk_warehouse.id)  
        available_quantity = request.data.get('available_quantity', warehouse_inventory.available_quantity)
        allotted_quantity = request.data.get("allotted_quantity", warehouse_inventory.allotted_quantity)
        total_quantity = request.data.get('total_quantity', warehouse_inventory.total_quantity)
        sold_quantity = request.data.get("sold_quantity", warehouse_inventory.sold_quantity)
        on_hand = request.data.get("on_hand", warehouse_inventory.on_hand)

         # Update Inventory object
        warehouse_inventory_data = {
            'available_quantity': available_quantity,
            'allotted_quantity': allotted_quantity,
            'total_quantity': total_quantity,
            'sold_quantity': sold_quantity,
            'product_total_valuation': total_quantity * warehouse_inventory.fk_product.mrp,
            'updated_by': request.user.id,
            'fk_tag':fk_tag_ids
        }
        warehouse_inventory_serializer = WarehouseInventorySerializer(warehouse_inventory, data=warehouse_inventory_data, partial=True)
        if warehouse_inventory_serializer.is_valid():
            warehouse_inventory = warehouse_inventory_serializer.save()
        else:
            return Response(warehouse_inventory_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # # Create InventoryLog object
        inventory_log_data = {
            'fk_product': fk_product_id,
            'updated_by': request.user.id,
            'fk_warehouse': fk_warehouse_id,
            'fk_tag': fk_tag_ids,
            'reason': reason,
            'available_quantity': available_quantity,
            'allotted_quantity': allotted_quantity,
            'total_quantity': total_quantity,
            'sold_quantity': sold_quantity,
            'damage_quantity': damage_quantity,
            'on_hand': on_hand,
        }
        inventory_log_serializer = InventoryLogSerializer(data=inventory_log_data)
        if inventory_log_serializer.is_valid():
            inventory_log_serializer.save()
        else:
            return Response(inventory_log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(warehouse_inventory_serializer.data, status=status.HTTP_200_OK)

    
    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        pass
