from store_app.models.inventory_and_warehouse.inventory import InventoryLog,Inventory
from store_app.models.inventory_and_warehouse.warehouse import WarehouseInventory
from django.db.models import Sum

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


def create_or_update_inventory(instance):
    product = instance.fk_product
    inventories = WarehouseInventory.objects.filter(fk_product=product)

    print("DEBUG: Number of inventories found:", inventories.count())

    # Aggregate quantities across all warehouses
    total_available_quantity = inventories.aggregate(total_available=Sum('available_quantity'))['total_available'] or 0
    total_allotted_quantity = inventories.aggregate(total_allotted=Sum('allotted_quantity'))['total_allotted'] or 0
    total_total_quantity = inventories.aggregate(total_total=Sum('total_quantity'))['total_total'] or 0
    total_sold_quantity = inventories.aggregate(total_sold=Sum('sold_quantity'))['total_sold'] or 0
    total_on_hand = inventories.aggregate(total_on_hand=Sum('on_hand'))['total_on_hand'] or 0

    print("DEBUG: Aggregated quantities - available:", total_available_quantity, "allotted:", total_allotted_quantity, "total:", total_total_quantity, "sold:", total_sold_quantity, "on_hand:", total_on_hand)

    # Create or update the inventory record
    inventory, created = Inventory.objects.get_or_create(fk_product=product)
    inventory.available_quantity = total_available_quantity
    inventory.allotted_quantity = total_allotted_quantity
    inventory.total_quantity = total_total_quantity
    inventory.sold_quantity = total_sold_quantity
    inventory.on_hand = total_on_hand
    inventory.save()

    print("DEBUG: Inventory created or updated -", inventory)