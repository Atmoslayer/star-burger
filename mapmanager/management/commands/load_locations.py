import requests
from django.core.management.base import BaseCommand
from progress.bar import IncrementalBar
from requests import HTTPError

from foodcartapp.models import Restaurant
from mapmanager.models import MapPoint
from star_burger.settings import MAPS_API_KEY


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


def load_locations(order=None):
    try:
        if order:
            address = order.customer_address
            lat, lon = fetch_coordinates(MAPS_API_KEY, address)
            MapPoint.objects.update_or_create(
                address=address,
                lat=lat,
                lon=lon,
            )
        else:
            restaurants = Restaurant.objects.all()
            bar = IncrementalBar(f'Downloading coordinates', max=len(restaurants))
            for restaurant in restaurants:
                lat, lon = fetch_coordinates(MAPS_API_KEY, restaurant.address)
                MapPoint.objects.update_or_create(
                    address=restaurant.address,
                    lat=lat,
                    lon=lon,
                )
                bar.next()
    except HTTPError:
        pass

class Command(BaseCommand):
    help = 'Loads locations to DB'

    def handle(self, *args, **options):
        load_locations()

