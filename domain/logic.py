# Logique Métiers
from haversine import haversine

from geopy import Nominatim
locator = Nominatim(user_agent="low-fuel")

from data import *


def near_stations(latitude: float, longitude: float, radius: int, sell_points: List[SellPoint]):
    list_stations = []
    home_coordinates = (latitude, longitude)
    for sell_point in sell_points:
        station_address = sell_point.address
        station_coordinates = (station_address.latitude, station_address.longitude)
        distance = haversine(home_coordinates, station_coordinates)
        if distance <= radius:
            list_stations.append(sell_point)
    return list_stations


def fuel_from_station(list_stations: List[SellPoint]):
    list_fuel_price = []
    for station in list_stations:
        for price in station.prices:
            list_fuel_price.append((station, price.fuel_type, price))
    return list_fuel_price

def coord_to_store_name(latitude: float, logitude:float):
    location = locator.geocode(str(latitude) + "," + str(longitude))
    name = str(location).split(',')[0]
    return name    

def address_to_coord(Address):
    if locator.geocode(address) is not None:
        return location[1]
