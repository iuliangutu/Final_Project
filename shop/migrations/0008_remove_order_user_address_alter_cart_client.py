# Generated by Django 5.1.4 on 2024-12-15 08:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_username_profile_user'),
        ('shop', '0007_cart_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user_address',
        ),
        migrations.AlterField(
            model_name='cart',
            name='client',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile'),
        ),
    ]
