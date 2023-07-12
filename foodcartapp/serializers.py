from rest_framework import serializers
from rest_framework.serializers import Serializer
from phonenumber_field.serializerfields import PhoneNumberField

from foodcartapp.models import Product, Order, OrderProductItem


class ProductSerializer(Serializer):
    product = serializers.IntegerField(min_value=1, max_value=Product.objects.latest('id').id)
    quantity = serializers.IntegerField(min_value=1)

    def create(self, product_data, order):
        product = Product.objects.get(id=product_data['product'])
        product_item = OrderProductItem.objects.create(
            product=product,
            order=order,
            product_cost=product.price,
            product_quantity=product_data['quantity']
        )

        return product_item


class OrderSerializer(serializers.ModelSerializer):
    firstname = serializers.CharField(source='customer_first_name')
    lastname = serializers.CharField(source='customer_last_name')
    address = serializers.CharField(source='customer_address')
    phonenumber = PhoneNumberField(source='customer_phone_number')
    products = ProductSerializer(many=True, allow_empty=False)

    def create(self, validated_data):
        order = Order.objects.create(
            customer_first_name=validated_data['customer_first_name'],
            customer_last_name=validated_data['customer_last_name'],
            customer_phone_number=validated_data['customer_phone_number'],
            customer_address=validated_data['customer_address'],
        )

        serializer = ProductSerializer(data=validated_data['products'])
        for product_data in validated_data['products']:
            product = serializer.create(product_data, order=order)
        return order

    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'address', 'phonenumber', 'products']
