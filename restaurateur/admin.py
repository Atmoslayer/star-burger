from django.contrib import admin
from .models import Order, OrderProductItem


class OrderProductItemInline(admin.TabularInline):
    model = OrderProductItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = [
        'customer_first_name',
        'customer_last_name',
        'customer_phone_number'
        'customer_address'
    ]

    list_display = [
        'customer_first_name',
        'customer_last_name',
        'customer_address'
    ]

    inlines = [
        OrderProductItemInline
    ]

