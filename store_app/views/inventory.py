from store_app.models.inventory_and_warehouse.inventory import InventoryLog
from store_app.models.inventory_and_warehouse.warehouse import WarehouseInventory
from django.db.models import Sum
from rest_framework.viewsets import ModelViewSet
from store_app.serializers.inventory import InventorySerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from store_app.models.inventory_and_warehouse.inventory import Inventory
class InventoryView(ModelViewSet):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]
    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        pass
    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):
        pass
    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        pass
    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        pass
    

def create_inventory_log(instance,old_quantity,reason):
    tags = instance.fk_tag.all()
    # print(old_quantity,'old')
    print(reason)
    print(tags)
    old_quantity = int(old_quantity)
    # print(instance.available_quantity,'aivdi[sd]')
    adjusted = instance.available_quantity -old_quantity
    # print(adjusted,'adjusted')
    inventory_log = InventoryLog.objects.create(
        fk_product=instance.fk_product,
        updated_by=instance.updated_by,
        fk_warehouse=instance.fk_warehouse,
        product_name=instance.fk_product.name,
        username=instance.updated_by.username,
        warehouse_name=instance.fk_warehouse.name,
        tag_name=', '.join([tag.name for tag in tags]),
        reason=reason,
        available_quantity=instance.available_quantity,
        allotted_quantity=instance.allotted_quantity,
        total_quantity=instance.total_quantity,
        sold_quantity=instance.sold_quantity,
        damage_quantity=instance.damage_quantity,
        on_hand=instance.on_hand,
        adjusted_qty=instance.available_quantity - old_quantity,
    )

    # Instead of updating directly, add tags one by one
    for tag in tags:
        inventory_log.fk_tag.add(tag)