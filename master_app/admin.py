from django.contrib import admin

# Register your models here.

from master_app.models import Store,Domain,NewUser

admin.site.register(Store)
admin.site.register(Domain)
admin.site.register(NewUser)
