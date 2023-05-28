import json

from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from restaurateur.models import Order, OrderProductItem


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
    order, created = Order.objects.get_or_create(
        customer_first_name=data.get('firstname', ''),
        customer_last_name=data.get('lastname', ''),
        customer_phone_number=data.get('phonenumber', ''),
        customer_address=data.get('address', ''),
    )
    try:
        products = data['products']
        if not products:
            content = {'products': 'Этот список не может быть пустым.'}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
        for product in products:
            product = Product.objects.get(id=product.get('product', ''))
            for product_quantity in range(product.get('quantity', '')):
                OrderProductItem.objects.create(
                    order=order,
                    product=product
                )
    except AttributeError:
        content = {'products': 'Ожидался list со значениями, но был получен "str". '}
        return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
    except TypeError:
        content = {'products': 'Это поле не может быть пустым.'}
        return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
    except KeyError:
        content = {'products': 'Обязательное поле.'}
        return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

    return Response(data)

