from master_app.models import NewUser
from store_app.models import *
from store_app.models.product import Product
from store_app.models.tag import Tag


class OtherDetail(models.Model):
    name = models.CharField(max_length=255)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'other_detail'
        verbose_name_plural = 'other detail'


class Warehouse(models.Model):
    fk_user = models.ForeignKey(NewUser,verbose_name='Warehouse User',on_delete=models.CASCADE)
    fk_tag = models.ManyToManyField(Tag)
    fk_other_detail = models.ManyToManyField(OtherDetail,verbose_name='Other Details',null=True,blank=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    gst_num = models.CharField(max_length=100)
    total_capacity = models.IntegerField(default=0)
    available_capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'warehouse'
        verbose_name_plural = 'warehouses'


class WarehouseInventory(models.Model):
    fk_product = models.ForeignKey(Product, verbose_name='Warehouse Inventory Product', on_delete=models.CASCADE)
    fk_warehouse = models.ForeignKey(Warehouse, verbose_name='Warehouse', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(NewUser, verbose_name='Updated by user', on_delete=models.DO_NOTHING)
    fk_tag = models.ManyToManyField(Tag, verbose_name='Tag', null=True, blank=True)
    available_quantity = models.IntegerField(default=0)
    allotted_quantity = models.IntegerField(default=0)
    total_quantity = models.IntegerField(default=0)
    sold_quantity = models.IntegerField(default=0)
    product_total_valuation = models.BigIntegerField(default=0)
    on_hand= models.IntegerField(default=0)
    damage_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
    

        return f'Product is {self.fk_product.name} & it is in  Warehouse {self.fk_warehouse.name } ' 
    class Meta:
        db_table = 'warehouse_inventory'
        verbose_name_plural = 'warehouse inventory'
