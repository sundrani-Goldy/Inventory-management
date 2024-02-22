from django.db import models

from store_app.models.tag import Tag


class Category(models.Model):
    name = models.CharField(max_length=255)
    fk_tag = models.ForeignKey(Tag, verbose_name='Tag', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'Categories'

class Variant(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    fk_tag = models.ForeignKey(Tag, verbose_name='Tag', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'variant'
        verbose_name_plural = 'variants'


class ExtraDetails(models.Model):
    name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=4)
    unit = models.CharField(choices=[('kg', 'Kg'), ('cm','Cm'),('metre','Metre'),('inches','Inches'),('oz','Oz'),('litre','Litre'),('ml','ML'),('mm','MM'),('ton','Ton'),('grams','Grams')], max_length=100)
    fk_tag = models.ForeignKey(Tag, verbose_name='Tag', on_delete=models.DO_NOTHING)