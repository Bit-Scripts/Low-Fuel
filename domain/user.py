import dataclasses


@dataclasses.dataclass
class AboutUser:
    id: int
    first_name: str
    last_name: str


@dataclasses.dataclass
class AddressUser:
    id: int
    street: str
    post_code: int
    city: str
    radius: float
    latitude: float = 0.0
    longitude: float = 0.0


@dataclasses.dataclass
class TypeOfFuel:
    fuel: str


