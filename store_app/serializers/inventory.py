from rest_framework import serializers
from store_app.models import Inventory, InventoryLog
from datetime import datetime

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


class InventoryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryLog
        fields = '__all__'

    def create(self, validated_data):
        # Calculate total_value based on total_quantity and fk_product.mrp
        total_quantity = validated_data['total_quantity']
        mrp = validated_data['fk_product'].mrp
        total_value = total_quantity * mrp

        # Create Inventory record
        inventory_data = {
            'fk_product': validated_data['fk_product'],
            'available_quantity': validated_data['available_quantity'],
            'allotted_quantity': validated_data['allotted_quantity'],
            'total_quantity': total_quantity,
            'sold_quantity': validated_data['sold_quantity'],
            'total_value': total_value,
            'on_hand': validated_data['on_hand'],
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }   
        inventory = Inventory.objects.create(**inventory_data)

        return super().create(validated_data)


''''

'''
