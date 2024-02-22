from django.contrib import admin

# Register your models here.
from main_app.models.customer import Customer

admin.site.register(Customer)