from dataclasses import dataclass
from enum import Enum
from datetime import datetime, date
from uuid import UUID

from entities.common import Address
from entities.writable_entity import WritableEntity


class Gender(Enum):
    MALE = 'М'
    FEMALE = 'Ж'

@dataclass
class Client(WritableEntity):
    client_id: UUID
    name: str
    birthdate: date
    gender: Gender
    phone_number: str
    email: str
    residence_address: Address
    registration_dttm: datetime
