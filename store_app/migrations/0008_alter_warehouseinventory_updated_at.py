# Generated by Django 4.2.1 on 2024-03-22 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0007_alter_warehouse_fk_other_detail_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouseinventory',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
