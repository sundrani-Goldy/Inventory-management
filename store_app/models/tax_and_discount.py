from django.db import models

from store_app.models.tag import Tag


class Tax(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=3, decimal_places=2)
    fk_tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tax'
        verbose_name_plural = 'taxes'

class Discount(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=3, decimal_places=2)
    fk_tax = models.ForeignKey(Tax , on_delete=models.DO_NOTHING)