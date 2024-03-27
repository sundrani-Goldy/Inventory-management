from django.db import models, connection

from store_app.models.tag import Tag


class Category(models.Model):
    name = models.CharField(max_length=255)
    fk_tag = models.ManyToManyField(Tag, verbose_name='Tag')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'Categories'


class Variant(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    fk_tag = models.ManyToManyField(Tag, verbose_name='Tag')
    fk_product = models.ForeignKey('store_app.Product', verbose_name='Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'variant'
        verbose_name_plural = 'variants'

def product_image_upload_path(instance, filename):
    store_name = connection.schema_name
    return f'{store_name}/{filename}'
class VariantImage(models.Model):
    fk_variant = models.ForeignKey(Variant , verbose_name='Variant', on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to='variant_image_upload_path')

    def __str__(self):
        return self.image.name

class ExtraDetails(models.Model):
    name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=4)
    unit = models.CharField(
        choices=[('kg', 'Kg'), ('cm', 'Cm'), ('metre', 'Metre'), ('inches', 'Inches'), ('oz', 'Oz'), ('litre', 'Litre'),
                 ('ml', 'ML'), ('mm', 'MM'), ('ton', 'Ton'), ('grams', 'Grams')], max_length=100)
    fk_tag = models.ManyToManyField(Tag, verbose_name='Tag')
    fk_product = models.ForeignKey('store_app.Product', verbose_name='Product', on_delete=models.CASCADE)
