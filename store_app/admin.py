from django.contrib import admin

# Register your models here.
from store_app.models.product import Product, ProductImage
from store_app.models.product_detail import Category, Variant, ExtraDetails, VariantImage
from store_app.models.tag import Tag
from store_app.models.product_detail import Category ,Variant ,ExtraDetails
from store_app.models.tax_and_discount import Discount,Tax
from store_app.models.inventory_and_warehouse.warehouse import Warehouse,WarehouseInventory,OtherDetail
from store_app.models.inventory_and_warehouse.inventory import Inventory,InventoryLog
from store_app.models.tax_and_discount import Discount, Tax
from store_app.models.product_detail import Category ,Variant ,ExtraDetails
from store_app.models.tax_and_discount import Discount,Tax
from store_app.models.inventory_and_warehouse.warehouse import Warehouse,WarehouseInventory,OtherDetail
from store_app.models.inventory_and_warehouse.inventory import Inventory,InventoryLog



admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Variant)
admin.site.register(Discount)
admin.site.register(Tax)
admin.site.register(Tag)
admin.site.register(ExtraDetails)
admin.site.register(ProductImage)
admin.site.register(Warehouse)
admin.site.register(WarehouseInventory)
admin.site.register(OtherDetail)
class CustomInventoryLog(admin.ModelAdmin):
    # Define the fields you want to display in the admin interface
    list_display = ['product_name', 'warehouse_name', 'username', 'tag_name', 'reason', 'available_quantity','adjusted_qty', 'allotted_quantity', 'total_quantity', 'sold_quantity', 'damage_quantity', 'on_hand', 'created_at']

    def display_fk_warehouse(self, obj):
        return obj.fk_warehouse.name  # Assuming there's a 'name' field in the Warehouse model

    def display_fk_tag(self, obj):
        return ', '.join(tag.name for tag in obj.fk_tag.all())  # Assuming there's a 'name' field in the Tag model

# Register the custom admin class with the InventoryLog model
admin.site.register(InventoryLog, CustomInventoryLog)
admin.site.register(Inventory)
admin.site.register(VariantImage)
admin.site.register(VariantImage)
admin.site.register(Warehouse)
admin.site.register(WarehouseInventory)
admin.site.register(OtherDetail)

admin.site.register(InventoryLog)
admin.site.register(Inventory)

class CustomInventoryLog(admin.ModelAdmin):
    # Define the fields you want to display in the admin interface
    list_display = ['product_name', 'warehouse_name', 'username', 'tag_name', 'reason', 'available_quantity','adjusted_qty', 'allotted_quantity', 'total_quantity', 'sold_quantity', 'damage_quantity', 'on_hand', 'created_at']

    def display_fk_warehouse(self, obj):
        return obj.fk_warehouse.name  # Assuming there's a 'name' field in the Warehouse model

    def display_fk_tag(self, obj):
        return ', '.join(tag.name for tag in obj.fk_tag.all())  # Assuming there's a 'name' field in the Tag model

# Register the custom admin class with the InventoryLog model
admin.site.register(InventoryLog, CustomInventoryLog)
admin.site.register(Inventory)
