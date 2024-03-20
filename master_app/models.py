from django.db import models
from django.dispatch import receiver
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.auth.models import AbstractUser

class Store(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

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


class Domain(DomainMixin):
    pass

class NewUser(AbstractUser):
    type = models.CharField(max_length=100)
