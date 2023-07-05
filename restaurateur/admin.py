from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme

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

    def response_change(self, request, obj):
        next_url = request.GET.get('next', None)
        if url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure()
        ):
            return HttpResponseRedirect(request.GET['next'])

        else:
            return super(OrderAdmin, self).response_change(request, obj)
