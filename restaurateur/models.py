from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum
from phonenumber_field.modelfields import PhoneNumberField
from foodcartapp.models import Product


class OrderQuerySet(models.QuerySet):
    def fetch_with_order_cost(self):
        orders = self.annotate(cost=Sum('product_items__products_cost'))
        return orders


class Order(models.Model):
    objects = OrderQuerySet.as_manager()
    customer_first_name = models.CharField(
        'Имя клиента',
        max_length=50,
    )

    customer_last_name = models.CharField(
        'Фамилия клиента',
        max_length=50,
    )

    customer_address = models.CharField(
        'Адрес клиента',
        max_length=150,
    )

    customer_phone_number = PhoneNumberField('Номер телефона клиента')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.customer_first_name} {self.customer_last_name}, {self.customer_address}'


class OrderProductItem(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        verbose_name='Продукт',
        on_delete=models.CASCADE,
    )
    order = models.ForeignKey(
        Order,
        related_name='product_items',
        verbose_name='Заказ',
        on_delete=models.CASCADE,
    )
    products_cost = models.DecimalField(
        'Стоимость товаров',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'
