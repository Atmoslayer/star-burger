# Generated by Django 3.2.15 on 2023-07-03 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurateur', '0004_alter_orderproductitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproductitem',
            name='products_quantity',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]