from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum, F, Prefetch
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f'{self.restaurant.name} - {self.product.name}'


class OrderQuerySet(models.QuerySet):

    def fetch_with_restaurant(self):
        orders_with_restaurants = self.prefetch_related(
            Prefetch(
                'product_items',
                queryset=OrderProductItem.objects.prefetch_related(Prefetch(
                    'product',
                    queryset=Product.objects.prefetch_related(Prefetch(
                        'menu_items',
                        queryset=RestaurantMenuItem.objects.filter(availability=True).prefetch_related(
                            'restaurant'
                        )
                    ))
                ))
            )
        )
        return orders_with_restaurants

    def fetch_with_order_cost(self):
        orders_with_cost = self.annotate(cost=Sum(F('product_items__product_cost') * F('product_items__product_quantity')))
        return orders_with_cost


class Order(models.Model):
    objects = OrderQuerySet.as_manager()

    NOT_HANDLED = 'NH'
    HANDLED_BY_MANAGER = 'HM'
    HANDLED_BY_RESTAURANT = 'HR'
    HANDLED_BY_DELIVER = 'HD'
    DELIVERED = 'DD'

    CASH = 'CH'
    CARD = 'CD'
    NOT_SELECTED = 'NS'

    STATUS_CHOICES = [
        (NOT_HANDLED, 'Не обработан'),
        (HANDLED_BY_MANAGER, 'Обработан менеджером'),
        (HANDLED_BY_RESTAURANT, 'Собран рестораном'),
        (HANDLED_BY_DELIVER, 'Доставляется курьером'),
        (DELIVERED, 'Доставлен')
    ]

    PAYMENT_CHOICES = [
        (NOT_SELECTED, 'Не выбрано'),
        (CASH, 'Наличные'),
        (CARD, 'Карта')
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

    payment_method = models.CharField(
        'Способ оплаты',
        max_length=2,
        choices=PAYMENT_CHOICES,
        default=NOT_SELECTED,
        db_index=True
    )

    register_date = models.DateTimeField(
        'Дата и время регистрации заказа',
        default=timezone.now,
        db_index=True
    )

    call_date = models.DateTimeField(
        'Дата и время звонка',
        null=True,
        blank=True,
        db_index=True
    )

    deliver_date = models.DateTimeField(
        'Дата и время доставки',
        null=True,
        blank=True,
        db_index=True
    )

    comment = models.TextField(
        'Комментарий',
        max_length=300,
        blank=True,
        db_index=True
    )

    current_restaurant = models.ForeignKey(
        Restaurant,
        related_name='orders',
        verbose_name='Ресторан, который готовит заказ',
        on_delete=models.CASCADE,
        blank=True,
        null=True
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

