from rest_framework import serializers
from store_app.models import Inventory, InventoryLog
from datetime import datetime
from store_app.models.inventory_and_warehouse.warehouse import Warehouse
from django.db import transaction
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

    
class InventoryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryLog
        fields = '__all__'

    