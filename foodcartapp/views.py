from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .models import Product
from restaurateur.models import Order, OrderProductItem
from phonenumber_field.serializerfields import PhoneNumberField


class ProductSerializer(Serializer):
    product = serializers.IntegerField(min_value=1, max_value=Product.objects.latest('id').id)
    quantity = serializers.IntegerField(min_value=1)


class CustomerSerializer(serializers.ModelSerializer):
    firstname = serializers.CharField(source='customer_first_name')
    lastname = serializers.CharField(source='customer_last_name')
    address = serializers.CharField(source='customer_address')
    phonenumber = PhoneNumberField(source='customer_phone_number')
    products = ProductSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'address', 'phonenumber', 'products']


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['GET', 'POST'])
def register_order(request):
    data = request.data
    if data:
        serializer = CustomerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        order, created = Order.objects.get_or_create(
            customer_first_name=data.get('firstname', ''),
            customer_last_name=data.get('lastname', ''),
            customer_phone_number=data.get('phonenumber', ''),
            customer_address=data.get('address', ''),
        )
        products_data = data.get('products', '')
        for product_data in products_data:
            product = Product.objects.get(id=product_data.get('product', ''))
            for product_quantity in range(product_data.get('quantity', '')):
                OrderProductItem.objects.create(
                    order=order,
                    product=product
                )
    return Response(data)
