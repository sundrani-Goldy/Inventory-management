# Generated by Django 4.2.1 on 2024-03-08 06:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0004_alter_warehouse_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discount',
            name='fk_tax',
        ),
        migrations.AddField(
            model_name='discount',
            name='discount_option',
            field=models.CharField(choices=[('percentage', 'Percentage'), ('fixed_amount', 'Fixed Amount')], default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='discount',
            name='fk_tag',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.DO_NOTHING, to='store_app.tag'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='discount',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='fk_other_tax',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='store_app.tax', verbose_name='other tax'),
        ),
        migrations.DeleteModel(
            name='OtherTax',
        ),
    ]
