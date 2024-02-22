from django.contrib import admin
from master_app.models import Store, Domain, NewUser

class PublicSchemaAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if request.tenant.schema_name == 'public':
            return True
        return False

admin.site.register(Store, PublicSchemaAdmin)
admin.site.register(Domain, PublicSchemaAdmin)
admin.site.register(NewUser)
