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
from store_app.serializers.inventory import InventorySerializer,InventoryLogSerializer
from store_app.models.inventory_and_warehouse.inventory import Inventory,InventoryLog
from rest_framework.exceptions import ValidationError
from store_app.models.product import Product
from store_app.models.inventory_and_warehouse.warehouse import Warehouse
from store_app.models.product_detail import Tag
class InventoryLogView(ModelViewSet):
    queryset = InventoryLog.objects.all()
    serializer_class = InventoryLogSerializer
    # permission_classes = [IsAdminUser]
    # authentication_classes = [TokenAuthentication]


class InventoryView(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]


    def create(self, request, *args, **kwargs):
        product_id = request.data.get('fk_product')
        if Inventory.objects.filter(fk_product_id=product_id).exists():
            return Response({"error": "Product already exists in inventory."}, status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.get(id=product_id)

        available_quantity = request.data.get('available_quantity')
        allotted_quantity = request.data.get("allotted_quantity")
        total_quantity = request.data.get('total_quantity')
        sold_quantity = request.data.get("sold_quantity")
        damage_quantity = request.data.get("damage_quantity")
        on_hand = request.data.get("on_hand")
        reason = request.data.get("reason")
        fk_warehouse_id = request.data.get("fk_warehouse")
        # fk_warehouse_id = Warehouse.objects.get(id=fk_warehouses)
        fk_tag_ids = request.data.get("fk_tag")
        # fk_tag_ids = Tag.objects.get(id=fk_tag_id)

        # Create Inventory object
        inventory_data = {
            'fk_product': product_id,
            'available_quantity': available_quantity,
            'allotted_quantity': allotted_quantity,
            'total_quantity': total_quantity,
            'sold_quantity': sold_quantity,
            'total_value': total_quantity * product.mrp,
            'on_hand': on_hand
        }
        inventory_serializer = InventorySerializer(data=inventory_data)
        if inventory_serializer.is_valid():
            inventory = inventory_serializer.save()
        else:
            return Response(inventory_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create InventoryLog object
        inventory_log_data = {
            'fk_product': product_id,
            'updated_by': request.user.id,
            'fk_warehouse': fk_warehouse_id,
            "fk_tag":fk_tag_ids,
            'reason': reason,
            'available_quantity': available_quantity,
            'allotted_quantity': allotted_quantity,
            'total_quantity': total_quantity,
            'sold_quantity': sold_quantity,
            'damage_quantity': damage_quantity,
            'on_hand': on_hand
        }
        inventory_log_serializer = InventoryLogSerializer(data=inventory_log_data)
        if inventory_log_serializer.is_valid():
            inventory_log_serializer.save()
        else:
            # If InventoryLog creation fails, delete the Inventory object
            inventory.delete()
            return Response(inventory_log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(inventory_serializer.data, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        inventory_id = kwargs['pk']
        inventory = Inventory.objects.get(id=inventory_id)
        inventory_log = InventoryLog.objects.get(fk_product=inventory.fk_product)

        available_quantity = request.data.get('available_quantity', inventory.available_quantity)
        allotted_quantity = request.data.get("allotted_quantity", inventory.allotted_quantity)
        total_quantity = request.data.get('total_quantity', inventory.total_quantity)
        sold_quantity = request.data.get("sold_quantity", inventory.sold_quantity)
        damage_quantity = request.data.get("damage_quantity", inventory_log.damage_quantity)
        on_hand = request.data.get("on_hand", inventory.on_hand)
        reason = request.data.get("reason", inventory_log.reason)
        fk_warehouse_id = request.data.get("fk_warehouse", inventory_log.fk_warehouse.id)  
        fk_tag_ids = request.data.get("fk_tag", [tag.id for tag in inventory_log.fk_tag.all()]) 

        # Update Inventory object
        inventory_data = {
            'available_quantity': available_quantity,
            'allotted_quantity': allotted_quantity,
            'total_quantity': total_quantity,
            'sold_quantity': sold_quantity,
            'total_value': total_quantity * inventory.fk_product.mrp,
            'on_hand': on_hand
        }
        inventory_serializer = InventorySerializer(inventory, data=inventory_data, partial=True)
        if inventory_serializer.is_valid():
            inventory = inventory_serializer.save()
        else:
            return Response(inventory_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create InventoryLog object
        inventory_log_data = {
            'fk_product': inventory.fk_product.id,
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

        return Response(inventory_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        inventory_id = kwargs['pk']
        inventory = Inventory.objects.get(id=inventory_id)
        
        # Retrieve the most recent InventoryLog associated with the inventory
        inventory_logs = InventoryLog.objects.filter(fk_product=inventory.fk_product).order_by('-created_at')
        
        if inventory_logs.exists():
            inventory_log = inventory_logs.first()  # Get the most recent inventory log
            fk_tag_ids = [tag.pk for tag in inventory_log.fk_tag.all()]

            # Create InventoryLog object
            inventory_log_data = {
                'fk_product': inventory.fk_product.id,
                'updated_by': request.user.id,
                'fk_warehouse': inventory_log.fk_warehouse.id,
                'fk_tag': fk_tag_ids,  # Assuming there could be multiple tags
                'reason': inventory_log.reason,
                'available_quantity': inventory.available_quantity,
                'allotted_quantity': inventory.allotted_quantity,
                'total_quantity': inventory.total_quantity,
                'sold_quantity': inventory.sold_quantity,
                'damage_quantity': inventory_log.damage_quantity,
                'total_value': inventory.total_quantity * inventory.fk_product.mrp,
                'on_hand': inventory.on_hand,
            }
            inventory_log_serializer = InventoryLogSerializer(data=inventory_log_data)
            if inventory_log_serializer.is_valid():
                inventory_log_serializer.save()
                inventory.delete()
                return Response("Inventory Deleted Successfully", status=status.HTTP_200_OK)
            else:
                return Response(inventory_log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("No associated InventoryLog found", status=status.HTTP_404_NOT_FOUND)
