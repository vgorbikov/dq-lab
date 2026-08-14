from dataclasses import dataclass
from enum import Enum
from typing import List
from datetime import datetime, date
from uuid import UUID

from entities.common import Address, Price
from entities.writable_entity import WritableEntity


@dataclass
class OrderClient(WritableEntity):
    client_id: UUID
    name: str
    birthdate: date
    phone_number: str 
    email: str

@dataclass
class ProductSize(WritableEntity):
    length: int 
    width: int 
    height: int 

@dataclass
class OrderProduct(WritableEntity):
    product_id: UUID
    product_name: str
    weight_kg: int
    size: ProductSize
    sku: str
    price: Price

    def __hash__(self):
        return hash(self.product_id.hex)

@dataclass
class PickUpPoint(WritableEntity):
    point_id: UUID
    address: Address 
    open_date: date

class OrderStatus(Enum):
    CREATED = 'CREATED'
    PAYMENT_WAITING = 'PAYMENT_WAITING'
    PROCESSED = 'PROCESSED'
    READY_FOR_SHIP = 'READY_FOR_SHIP'
    DELIVERED = 'DELIVERED'
    READY_FOR_ISSUE = 'READY_FOR_ISSUE'
    FINISHED = 'FINISHED'
    CANCELLED = 'CANCELLED'

@dataclass
class Order(WritableEntity):
    order_id: UUID
    positions: List["OrderPosition"]
    client: OrderClient
    status: OrderStatus
    pick_up_point: PickUpPoint
    total_price: Price
    track_number: str
    creation_dttm: datetime
    update_dttm: datetime

@dataclass
class OrderPosition(WritableEntity):
    product: OrderProduct
    quantity: int
