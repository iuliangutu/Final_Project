# Generated by Django 5.1.4 on 2025-02-02 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_orderline_order_alter_orderline_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderline',
            name='product_price',
            field=models.IntegerField(),
        ),
    ]
