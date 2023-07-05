from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum, F
from phonenumber_field.modelfields import PhoneNumberField
from foodcartapp.models import Product


class OrderQuerySet(models.QuerySet):
    def fetch_with_order_cost(self):
        orders = self.annotate(
            cost=Sum(F('product_items__product_cost') * F('product_items__product_quantity'))
        )
        return orders


class Order(models.Model):
    objects = OrderQuerySet.as_manager()

    NOT_HANDLED = 'NH'
    HANDLED_BY_MANAGER = 'HM'
    HANDLED_BY_RESTAURANT = 'HR'
    HANDLED_BY_DELIVER = 'HD'
    DELIVERED = 'DD'
    STATUS_CHOICES = [
        (NOT_HANDLED, 'Не обработан'),
        (HANDLED_BY_MANAGER, 'Обработан менеджером'),
        (HANDLED_BY_RESTAURANT, 'Собран рестораном'),
        (HANDLED_BY_DELIVER, 'Доставляется курьером'),
        (DELIVERED, 'Доставлен')
    ]

    status = models.CharField(
        'Статус',
        max_length=2,
        choices=STATUS_CHOICES,
        default=NOT_HANDLED,
        db_index=True
    )

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

    register_date = models.DateTimeField(
        'Дата и время регистрации заказа',
        default=timezone.now,
        db_index=True
    )

    call_date = models.DateTimeField(
        'Дата и время звонка',
        null=True,
        db_index=True
    )

    deliver_date = models.DateTimeField(
        'Дата и время доставки',
        null=True,
        db_index=True
    )

    comment = models.TextField(
        'Комментарий',
        max_length=300,
        blank=True,
        db_index=True
    )

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
    product_cost = models.DecimalField(
        'Цена продукта',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    product_quantity = models.IntegerField(
        'Количество продуктов',
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'
