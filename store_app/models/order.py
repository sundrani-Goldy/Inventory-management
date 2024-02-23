from django.db import models
from store_app.models import *



class OrderDetail(models.Model):
    fk_product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(max_length=255)
    discount = models.DecimalField(max_digits=3, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.fk_product.name
    
    class Meta:
        db_table = 'order_detail'
        verbose_name_plural = 'order details'


class Order(models.Model):
    fk_warehouse = models.ForeignKey(Warehouse,verbose_name="Warehouese", on_delete=models.DO_NOTHING)
    fk_customer = models.ForeignKey(Customer,verbose_name="Customer", on_delete=models.DO_NOTHING)
    fk_order_detail = models.ForeignKey(OrderDetail,verbose_name ,on_delete=models.DO_NOTHING)
    fk_tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    fk_discount = models.ForeignKey(Discount, on_delete=models.DO_NOTHING)
    fk_other_tax = models.ForeignKey(OtherTax, on_delete=models.DO_NOTHING)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.fk_customer.name
    
    class Meta:
        db_table = 'order'
        verbose_name_plural = 'orders'