# Generated by Django 5.1.4 on 2024-12-14 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_rename_provider_seller_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller',
            name='brand',
        ),
    ]