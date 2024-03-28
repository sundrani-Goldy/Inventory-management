from rest_framework import serializers
from store_app.models import Inventory, InventoryLog
from datetime import datetime
from store_app.models.inventory_and_warehouse.warehouse import Warehouse
from django.db import transaction
from store_app.serializers import product,tag,warehouse
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['fk_product'] = product.ProductSerializer(instance.fk_product).data
        return representation

    
class InventoryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryLog
        fields = '__all__'

    