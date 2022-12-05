# Logique Métiers
from haversine import haversine

from data import *


def near_stations(latitude: float, longitude: float, radius: int, sell_points: List[SellPoint]):
    list_stations = []
    for sell_point in sell_points:
        home_coordinates = (latitude, longitude)
        station_address = sell_point.address
        station_coordinates = (station_address.latitude, station_address.longitude)
        distance = haversine(home_coordinates, station_coordinates)
        if distance <= radius:
            list_stations.append(sell_point)
    return list_stations


def infos_from_station(list_stations: List[SellPoint], prices: List[Price], fuels_type: List[FuelType]):
    list_fuel_price = []
    for station in list_stations:
        for price in prices:
            for fuel_type in fuels_type:
                if station.id == price.id and fuel_type.value == price.name:
                    list_fuel_price.append(station, price)
    return list_fuel_price

