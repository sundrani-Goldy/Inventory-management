from django.contrib import admin

# Register your models here.
from store_app.models.product import Product,ProductImage
from store_app.models.tag import Tag
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
admin.site.register(InventoryLog)
admin.site.register(Inventory)