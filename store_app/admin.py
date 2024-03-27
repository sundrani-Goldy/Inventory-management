from django.contrib import admin

# Register your models here.
from store_app.models.product import Product, ProductImage
from store_app.models.product_detail import Category, Variant, ExtraDetails
from store_app.models.tag import Tag
from store_app.models.tax_and_discount import Discount, Tax

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Variant)
admin.site.register(Discount)
admin.site.register(Tax)
admin.site.register(Tag)
admin.site.register(ExtraDetails)
admin.site.register(ProductImage)
