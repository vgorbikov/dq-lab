from dataclasses import dataclass
from enum import Enum
from datetime import datetime, date
from uuid import UUID

from entities.common import Address



class Gender(Enum):
    MALE = 'М'
    FEMALE = 'Ж'

@dataclass
class Client():
    client_id: UUID
    name: str
    birthdate: date
    gender: Gender
    phone_number: str
    email: str
    residence_address: Address
    registration_dttm: datetime
