from store_app.models.inventory_and_warehouse.inventory import InventoryLog
from store_app.models.inventory_and_warehouse.warehouse import WarehouseInventory

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