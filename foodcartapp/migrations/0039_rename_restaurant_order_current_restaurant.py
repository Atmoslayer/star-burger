# Generated by Django 3.2.15 on 2023-07-11 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_order_orderproductitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='restaurant',
            new_name='current_restaurant',
        ),
    ]
