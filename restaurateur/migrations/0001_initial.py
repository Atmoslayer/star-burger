# Generated by Django 3.2.15 on 2023-05-18 18:43

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('foodcartapp', '0037_auto_20210125_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_first_name', models.CharField(max_length=50, verbose_name='Имя клиента')),
                ('customer_last_name', models.CharField(max_length=50, verbose_name='Фамилия клиента')),
                ('customer_address', models.CharField(max_length=150, verbose_name='Адрес клиента')),
                ('customer_phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона клиента')),
                ('product', models.ManyToManyField(related_name='orders', to='foodcartapp.Product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
    ]