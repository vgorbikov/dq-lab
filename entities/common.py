from dataclasses import dataclass
from enum import Enum



class Currency(Enum):
    RUB = "Российский рубль"
    USD = "Доллар США"
    BYN = "Белорусский рубль"

@dataclass
class Price():
    amount_value: int
    currency: Currency

@dataclass
class Address():
    country: str
    region: str 
    city: str
    street: str
    house: str
    postal_code: str
