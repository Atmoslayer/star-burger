# Generated by Django 3.2.15 on 2023-07-05 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurateur', '0011_order_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='call_date',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата и время звонка'),
        ),
        migrations.AlterField(
            model_name='order',
            name='deliver_date',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата и время доставки'),
        ),
    ]
