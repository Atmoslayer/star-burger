# Generated by Django 3.2.15 on 2023-07-05 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurateur', '0008_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, max_length=300, verbose_name='Комментарий'),
        ),
    ]
