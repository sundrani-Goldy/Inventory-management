from django.db import models
from store_app.models import *
from store_app.models.inventory_and_warehouse.warehouse import Warehouse
from store_app.models.tax_and_discount import Discount,OtherTax
from store_app.models.tag import Tag
from store_app.models.product import Product


class OrderDetail(models.Model):
    fk_product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2 , default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.fk_product.name
    
    class Meta:
        db_table = 'order_detail'
        verbose_name_plural = 'order details'


class Order(models.Model):
    fk_warehouse = models.ForeignKey(Warehouse,verbose_name="Warehouese", on_delete=models.DO_NOTHING)
    fk_customer = models.ForeignKey(Customer,verbose_name="Customer", on_delete=models.DO_NOTHING)
    fk_order_detail = models.ManyToManyField(OrderDetail,verbose_name = "product order detail" )
    fk_tag = models.ManyToManyField(Tag , verbose_name="tag")
    sub_total = models.DecimalField(max_digits=10, decimal_places=2 , verbose_name="sub total")
    fk_discount = models.ForeignKey(Discount, on_delete=models.DO_NOTHING , null=True, blank=True , verbose_name="discount")
    fk_other_tax = models.ForeignKey(OtherTax, on_delete=models.DO_NOTHING , null=True, blank=True , verbose_name="other tax")
    final_price = models.DecimalField(max_digits=10, decimal_places=2 , verbose_name="final bill price")

    def __str__(self):
        return self.fk_customer.name
    
    class Meta:
        db_table = 'order'
        verbose_name_plural = 'orders'