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
    fk_product = models.ForeignKey(Product,verbose_name='Log of inventory product',on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(NewUser,verbose_name='Updated by User',on_delete=models.DO_NOTHING)
    fk_warehouse = models.ForeignKey(Warehouse,verbose_name='Log of warehouse',on_delete=models.DO_NOTHING)
    fk_tag = models.ManyToManyField(Tag)
    product_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    warehouse_name = models.CharField(max_length=200)
    tag_name = models.CharField(max_length=200)
    reason = models.CharField(max_length=200,choices=[('Coorelation',"Coolreation"),('Count',"Count"),('Recieved',"Recieved"),('Damaged',"Damaged"),('Return Restock',"Return Restock"),('Theft or loss',"Theft or loss"),('Promotion or donation',"Promotion or donation")]) #if needed to add default just add  default='Coorelation'
    available_quantity = models.IntegerField(default=0)
    allotted_quantity = models.IntegerField(default=0)
    total_quantity = models.IntegerField(default=0)
    sold_quantity=models.IntegerField(default=0)
    damage_quantity = models.IntegerField(default=0)
    on_hand= models.IntegerField(default=0)
    adjusted_qty = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.fk_product.name
    
    class Meta:
        db_table = 'inventory_log'
        verbose_name_plural = 'inventory log'
    

