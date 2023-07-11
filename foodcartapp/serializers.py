from rest_framework import serializers
from rest_framework.serializers import Serializer
from phonenumber_field.serializerfields import PhoneNumberField

from foodcartapp.models import Product
from restaurateur.models import Order


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
