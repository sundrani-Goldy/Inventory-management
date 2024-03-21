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


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Check if there's only one warehouse left
        if Warehouse.objects.count() == 1:
            return Response({"Cannot delete the only remaining warehouse."}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
        return Response( "Warehouse Deleted Successfully",status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        pass


        

    
class WarehouseInventoryView(ModelViewSet):
    serializer_class = WarehouseInventorySerializer
    queryset = WarehouseInventory.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]
    