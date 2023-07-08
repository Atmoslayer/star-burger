from django.db import models
from django.utils import timezone


class MapPoint(models.Model):
    address = models.CharField(
        'Адрес',
        max_length=100,
        blank=True,
    )
    lat = models.FloatField(max_length=10, verbose_name='Широта')
    lon = models.FloatField(max_length=10, verbose_name='Долгота')
    call_date = models.DateTimeField(
        'Дата создания записи',
        default=timezone.now,
        db_index=True
    )

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.address


