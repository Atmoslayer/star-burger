from django.contrib import admin

from mapmanager.models import MapPoint


@admin.register(MapPoint)
class MapPointAdmin(admin.ModelAdmin):
    list_display = [
        'address',
        'lat',
        'lon',
        'call_date'
    ]
