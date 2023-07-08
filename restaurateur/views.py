from collections import Counter

import requests
from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from requests import HTTPError
from geopy import distance

from foodcartapp.models import Product, Restaurant, RestaurantMenuItem
from mapmanager.models import MapPoint
from restaurateur.models import Order
from star_burger.settings import MAPS_API_KEY


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    order_items = []
    orders = Order.objects.exclude(status='DD').fetch_with_restaurant().fetch_with_order_cost().order_by('-status')
    for order in orders:
        order_restaurants = {}
        current_restaurant = ''
        if not order.restaurant:
            products_restaurants = []
            product_items = order.product_items.all()
            for product_item in product_items:
                product = product_item.product
                product_restaurants = RestaurantMenuItem.objects.filter(product=product, availability=True)
                for product_restaurant in product_restaurants:
                    products_restaurants.append(product_restaurant.restaurant)
            product_quantity = len(product_items)
            restaurants_counter = Counter(products_restaurants)
            for restaurant in restaurants_counter.keys():
                if restaurants_counter[restaurant] == product_quantity:
                    restaurant_location = MapPoint.objects.get(address=restaurant.address)
                    order_location = MapPoint.objects.get(address=order.customer_address)
                    if restaurant_location and order_location:
                        restaurant_coordinates = (restaurant_location.lat, restaurant_location.lon)
                        order_coordinates = (order_location.lat, order_location.lon)
                        order_distance = round(distance.distance(restaurant_coordinates, order_coordinates).km, 2)
                    else:
                        order_distance = None
                    order_restaurants[order_distance] = restaurant.name

        else:
            current_restaurant = order.restaurant.name
            order.status = 'HM'
            order.save()
        order_items.append(
            {
                'id': order.id,
                'customer_first_name': order.customer_first_name,
                'customer_last_name': order.customer_last_name,
                'customer_phone_number': order.customer_phone_number,
                'customer_address': order.customer_address,
                'comment': order.comment,
                'status': order.get_status_display(),
                'cost': order.cost,
                'payment_method': order.get_payment_method_display(),
                'restaurants': sorted(order_restaurants.items()),
                'current_restaurant': current_restaurant
            }
        )

    return render(request, template_name='order_items.html', context={
        'order_items': order_items,
    })
