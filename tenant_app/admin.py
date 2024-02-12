from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from .models import *


class CustomStoreAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.exclude(name='public')
        if request.tenant.schema_name != 'public':
            queryset = queryset.filter(name=request.tenant.schema_name)

        return queryset

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser and request.tenant.schema_name == 'public':
            return True

        return False

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser and request.tenant.schema_name == 'public':
            if obj is None:
                return []
            return [field.name for field in self.model._meta.fields if field.name != 'is_active']

        return [field.name for field in self.model._meta.fields]


admin.site.register(Store, CustomStoreAdmin)
