import os
import sys

# setting path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# Logique Métiers
from haversine import haversine

from geopy import Nominatim

locator = Nominatim(user_agent="low-fuel")

from domain.data import *


def near_stations(home_latitude: float, home_longitude: float, radius: int, id_sell_point: str, sell_point_latitude: int, sell_point_longitude: int):
    distance = distance_between(home_latitude, home_longitude, sell_point_latitude, sell_point_longitude)
    if float(distance) <= float(radius):
        return True


def fuel_from_station(list_stations: List[SellPoint]):
    list_fuel_price = []
    for station in list_stations:
        for price in station.prices:
            list_fuel_price.append((station, price.fuel_type, price))
    return list_fuel_price


def coord_to_store_name(latitude: float, longitude: float):
    location = locator.geocode((str(latitude) + "," + str(longitude)), timeout=None)
    name = str(location).split(',')[0]
    return name


def address_to_coord(address):
    location = locator.geocode(address, timeout=None)
    if location is not None:
        return location[1]


def distance_between(home_latitude: float, home_longitude: float, sell_point_latitude: float, sell_point_longitude: float):
    home_coord = (home_latitude, home_longitude)
    sell_point_coord = (sell_point_latitude, sell_point_longitude)
    distance = haversine(home_coord, sell_point_coord)
    return distance


def stringtoint(hex: str):
    return int(hex,16)


def hextofloat(hex: int):
    return float(stringtoint(hex))


def colorHtmlToKivy(html: str):
    if len(html) == 7:
        red = hextofloat(html[1:3]) / 255.0
        green = hextofloat(html[3:5]) / 255.0
        blue = hextofloat(html[5:7]) / 255.0
        return tuple((red, green, blue))
    if len(html) == 9:
        alpha = hextofloat(html[7:9]) / 255.0
        return tuple((red, green, blue, alpha))
        