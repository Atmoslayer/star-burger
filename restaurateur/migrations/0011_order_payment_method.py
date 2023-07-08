# Generated by Django 3.2.15 on 2023-07-05 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurateur', '0010_auto_20230705_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('NS', 'Не выбрано'), ('CH', 'Наличные'), ('CD', 'Карта')], db_index=True, default='NS', max_length=2, verbose_name='Способ оплаты'),
        ),
    ]