# Generated by Django 5.1.4 on 2024-12-15 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_remove_order_user_address_alter_cart_client'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderline',
            old_name='number_of_products',
            new_name='quantity',
        ),
    ]