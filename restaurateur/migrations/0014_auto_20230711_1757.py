# Generated by Django 3.2.15 on 2023-07-11 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurateur', '0013_order_restaurant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproductitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderproductitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderProductItem',
        ),
    ]
