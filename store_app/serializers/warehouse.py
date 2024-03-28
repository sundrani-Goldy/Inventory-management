from rest_framework import serializers
from store_app.models.product_detail import Tag
from store_app.models.inventory_and_warehouse.warehouse import Warehouse,WarehouseInventory,OtherDetail
from store_app.serializers.product_details import *
from store_app.serializers.product import *

from master_app.models import NewUser
from store_app.models.inventory_and_warehouse.inventory import InventoryLog

class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields =['id','username','email','first_name','last_name']
class OtherDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OtherDetail
        fields = '__all__'


class WarehouseSerializer(serializers.ModelSerializer):
    fk_other_detail = serializers.PrimaryKeyRelatedField(queryset=OtherDetail.objects.all(),many=True)
    fk_tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),many=True)
    fk_user = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all())
    class Meta:
        model = Warehouse
        fields = '__all__'

    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['fk_other_detail'] = OtherDetailSerializer(instance.fk_other_detail.all(), many=True).data
        representation['fk_tag'] = TagSerializer(instance.fk_tag.all(), many=True).data
        representation['fk_user'] = NewUserSerializer(instance.fk_user).data
        return representation



class WarehouseInventorySerializer(serializers.ModelSerializer):
    fk_tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),many=True)
    fk_warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())
    updated_by = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all())
    fk_product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = WarehouseInventory
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['fk_tag'] = OtherDetailSerializer(instance.fk_tag.all(), many=True).data
        representation['fk_warehouse'] = WarehouseSerializer(instance.fk_warehouse).data
        representation['updated_by'] = NewUserSerializer(instance.updated_by).data

        return representation
