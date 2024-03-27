from rest_framework import serializers

from store_app.models import Warehouse, WarehouseInventory, OtherDetail


class OtherDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherDetail
        fields = '__all__'


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class WarehouseInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseInventory
        fields = '__all__'
