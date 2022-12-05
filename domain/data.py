# Classes métiers
from datetime import datetime, time
from enum import Enum
from dataclasses import dataclass
from typing import List, Union


# Gazole, SP95, SP98, GPLc, E10, E85
# Diesel, SP95, SP98, LPGc, E10, E85
class FuelType(Enum):
    DIESEL = "Gazole"
    SP95 = "SP95"
    SP98 = "SP98"
    LGPC = "GPLc"
    E10 = "E10"
    E85 = "E85"


@dataclass
class Price:
    id: int
    name: str
    last_updated: datetime
    value: float


@dataclass
class Address:
    street: str
    post_code: int
    city: str
    latitude: float
    longitude: float


@dataclass
class Service:
    name: str


class WeekDay(Enum):
    MONDAY = 1, "Lundi"
    TUESDAY = 2, "Mardi"
    WEDNESDAY = 3, "Mercredi"
    THURSDAY = 4, "Jeudi"
    FRIDAY = 5, "Vendredi"
    SATURDAY = 6, "Samedi"
    SUNDAY = 7, "Dimanche"


@dataclass
class Hour:
    opening: Union[int, int]
    closing: Union[int, int]


@dataclass
class DayHours:
    day: WeekDay
    closed: bool
    hours: List[Hour]


@dataclass
class WeekHours:
    is_24_24: bool
    day_hours: List[DayHours]


@dataclass
class SellPoint:
    id: int
    address: Address
    week_hours: WeekHours
    services: List[Service]
