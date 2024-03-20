from rest_framework import serializers
from store_app.models import Inventory, InventoryLog
from datetime import datetime
from store_app.models.inventory_and_warehouse.warehouse import Warehouse
from django.db import transaction
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
    
    def create(self, validated_data):
        fk_product = validated_data['fk_product']

        # Check if the product already exists in the inventory
        if Inventory.objects.filter(fk_product=fk_product).exists():
            raise serializers.ValidationError("Product already exists in inventory.")
        
        inventory = super().create(validated_data)
        total_quantity = validated_data['total_quantity']
        total_value = total_quantity * validated_data['fk_product'].mrp

        inventory_data = {
            'fk_product': fk_product,
            'fk_warehouse': validated_data.get('fk_warehouse'),
            'updated_by': self.context['request'].user,
            'reason': validated_data.get('reason'),
            'available_quantity': validated_data['available_quantity'],
            'allotted_quantity': validated_data['allotted_quantity'],
            'total_quantity': total_quantity,
            'sold_quantity': validated_data['sold_quantity'],
            'damage_quantity': validated_data['damage_quantity'],
            'on_hand': validated_data['on_hand'],
            'reason':validated_data['reason']
        }   

        # Create InventoryLog record
        with transaction.atomic():
            inventory_log = InventoryLog.objects.create(**inventory_data)

            # Handle tags
            tags = validated_data.get('fk_tag', [])  # Assuming fk_tag is a ManyToManyField in InventoryLog
            inventory_log.fk_tag.set(tags)

        inventory.total_value = total_value
        inventory.save()

        return inventory
    

class InventoryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryLog
        fields = '__all__'

    