from dataclasses import dataclass
from enum import Enum
from typing import List
from datetime import datetime, date
from uuid import UUID

from entities.common import Price
from entities.writable_entity import WritableEntity

@dataclass
class ProductSize():
    length: int 
    width: int 
    height: int 

@dataclass
class ProductCategory(WritableEntity):
    category_id: int
    category_name: str
    description: str
    products: List["Product"]

@dataclass
class Product(WritableEntity):
    product_id: UUID
    product_name: str 
    description: str
    category: ProductCategory 
    weight_kg: int 
    sku: str 
    size: ProductSize
    price: Price

    def __hash__(self):
        return hash(self.product_id.hex)

@dataclass
class Stock(WritableEntity):
    product: Product
    quantity: int 
    last_update: datetime

    def __hash__(self):
        return hash(self.product.product_id.hex)

@dataclass
class SupplyItem(WritableEntity):
    product: Product
    quantity: int
    batch_number: str
    
@dataclass
class Supply(WritableEntity):
    supply_id: UUID
    items: List[SupplyItem]
    supply_datetime: datetime

@dataclass
class ShipmentItem(WritableEntity):
    product: Product
    quantity: int

@dataclass
class Shipment(WritableEntity):
    shipment_id: UUID
    items: List[ShipmentItem]
    shipment_datetime: datetime
