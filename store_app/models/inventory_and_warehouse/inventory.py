from django.db import models
from store_app.models import *
from master_app.models import NewUser
from store_app.models.product import Product
from store_app.models.tag import Tag
from store_app.models.inventory_and_warehouse.warehouse import Warehouse


class Inventory(models.Model):
    fk_product = models.ForeignKey(Product,verbose_name='Inventory Product',on_delete=models.CASCADE)
    available_quantity = models.IntegerField(default=0)
    allotted_quantity = models.IntegerField(default=0)
    total_quantity = models.IntegerField(default=0)
    sold_quantity=models.IntegerField(default=0)
    total_value = models.IntegerField(default=0)
    on_hand= models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fk_product.name
    
    class Meta:
        db_table = 'inventory'
        verbose_name_plural = 'inventory'



class InventoryLog(models.Model):
    fk_product = models.ForeignKey(Product,verbose_name='Log of inventory product',on_delete=models.CASCADE)
    updated_by = models.ForeignKey(NewUser,verbose_name='Updated by User',on_delete=models.CASCADE)
    fk_warehouse = models.ForeignKey(Warehouse,verbose_name='Log of warehouse',on_delete=models.CASCADE)
    fk_tag = models.ManyToManyField(Tag)
    reason = models.CharField(max_length=200)
    available_quantity = models.IntegerField(default=0)
    allotted_quantity = models.IntegerField(default=0)
    total_quantity = models.IntegerField(default=0)
    sold_quantity=models.IntegerField(default=0)
    damage_quantity = models.IntegerField(default=0)
    on_hand= models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fk_product.name
    
    class Meta:
        db_table = 'inventory_log'
        verbose_name_plural = 'inventory log'
    

