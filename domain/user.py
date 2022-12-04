import dataclasses


@dataclasses
class AboutUser:
    id: int
    first_name: str
    last_name: str


@dataclasses
class AddressUser:
    id: int
    street: str
    post_code: int
    city: str
    latitude: float
    longitude: float


@dataclasses
class TypeOfFuel:
    fuel: str
