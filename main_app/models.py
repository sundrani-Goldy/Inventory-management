from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobile_number = models.BigIntegerField()
    email = models.EmailField(null=True,blank=True)
    company_name = models.CharField(max_length=200,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    pincode=models.IntegerField(null=True,blank=True)


    def __str__(self):
        return self.name
        
    class Meta:
        db_table = 'customer'
        verbose_name_plural = 'customer'