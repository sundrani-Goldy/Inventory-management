from django.db import connection
from django.db import models

from store_app.models.product_detail import Category
from store_app.models.tag import Tag
from store_app.models.tax_and_discount import Tax, Discount


class Product(models.Model):
    fk_category = models.ManyToManyField(Category, verbose_name='product category')
    fk_tag = models.ManyToManyField(Tag, verbose_name='product tag')
    name = models.CharField(max_length=255, verbose_name='product name')
    description = models.TextField(verbose_name='product description')
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='product base price')
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='product selling price')
    mrp = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='product MRP')
    fk_tax = models.ManyToManyField(Tax, verbose_name='product Tax', blank=True, null=True)
    discount = models.ManyToManyField(Discount, verbose_name='product Discount', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='product creation date')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        verbose_name_plural = 'products'


def product_image_upload_path(instance, filename):
    store_name = connection.schema_name
    return f'{store_name}/{filename}'


class ProductImage(models.Model):
    image = models.FileField(upload_to=product_image_upload_path)
    fk_product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.fk_product.name

