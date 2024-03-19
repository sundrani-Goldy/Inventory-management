from django.db import models
from django.db.models.signals import post_migrate,post_save
from django.dispatch import receiver
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.auth.models import AbstractUser

class Store(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    address = models.TextField()
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    gst_num = models.CharField(max_length=100)
    total_capacity = models.IntegerField(default=0)
    available_capacity = models.IntegerField(default=0)
    auto_create_schema = True
    auto_drop_schema = True

    def save(self, *args, **kwargs):
        super(Store, self).save(*args, **kwargs)

        existing_domain = Domain.objects.filter(domain=self.schema_name).first()
        if existing_domain:
            existing_domain.tenant = self
            existing_domain.save()
        else:
            domain = Domain()
            domain.tenant = self

            if self.schema_name == 'public':
                pass
            else:
                domain.is_primary = False
                school = Store.objects.get(schema_name='public')
                public_domain = Domain.objects.get(tenant=school)
                domain.domain = self.schema_name + "." + public_domain.domain
                domain.save()

@receiver(post_migrate, sender=Store)
def create_warehouse(sender, instance=None, **kwargs):

    from store_app.models.inventory_and_warehouse.warehouse import Warehouse
    
    if instance.schema_name != 'public':
        Warehouse.objects.using(instance.schema_name).create(
            name=instance.name,
            address=instance.address,
            contact=instance.contact,
            email=instance.email,
            gst_num=instance.gst_num,
            total_capacity=instance.total_capacity,
            available_capacity=instance.available_capacity
        )

class Domain(DomainMixin):
    pass

class NewUser(AbstractUser):
    type = models.CharField(max_length=100)
