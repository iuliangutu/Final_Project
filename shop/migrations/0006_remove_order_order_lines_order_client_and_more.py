# Generated by Django 5.1.4 on 2024-12-15 08:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_username_profile_user'),
        ('shop', '0005_remove_order_client_remove_orderline_product_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_lines',
        ),
        migrations.AddField(
            model_name='order',
            name='client',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='accounts.profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderline',
            name='product_price',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.order'),
        ),
    ]
