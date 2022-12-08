# Classes métiers
import dataclasses
from datetime import datetime, time
from enum import Enum
from typing import List, Union, Optional


# Gazole, SP95, SP98, GPLc, E10, E85
# Diesel, SP95, SP98, LPGc, E10, E85
class FuelType(Enum):
    DIESEL = "Gazole"
    SP95 = "SP95"
    SP98 = "SP98"
    LGPC = "GPLc"
    E10 = "E10"
    E85 = "E85"


@dataclasses.dataclass
class Price:
    id: int
    fuel_type: FuelType
    last_updated: datetime
    value: float


@dataclasses.dataclass
class Address:
    street: str
    post_code: int
    city: str
    latitude: float
    longitude: float


@dataclasses.dataclass
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


@dataclasses.dataclass
class Hour:
    opening: str
    closing: str


@dataclasses.dataclass
class DayHours:
    day: WeekDay
    closed: bool
    hours: List[Hour]


@dataclasses.dataclass
class WeekHours:
    is_24_24: bool
    day_hours: List[DayHours]


@dataclasses.dataclass
class SellPoint:
    id: int
    name: Optional[str]
    address: Address
    week_hours: WeekHours
    prices: List[Price]
    services: List[Service]
