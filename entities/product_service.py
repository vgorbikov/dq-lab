from dataclasses import dataclass
from enum import Enum
from typing import List
from datetime import datetime, date
from uuid import UUID

from entities.common import Price

@dataclass
class ProductSize():
    length: int 
    width: int 
    height: int 

@dataclass
class ProductCategory():
    category_id: int
    category_name: str
    description: str
    products: List["Product"]

@dataclass
class Product():
    product_id: UUID
    product_name: str 
    description: str
    category: ProductCategory 
    weight_kg: int 
    sku: str 
    size: ProductSize
    price: Price

@dataclass
class Stock():
    product: Product
    quantity: int 
    last_update: datetime

@dataclass
class SupplyItem():
    product: Product
    quantity: int
    batch_number: str
    
@dataclass
class Supply():
    supply_id: UUID
    items: List[SupplyItem]
    supply_datetime: datetime

@dataclass
class ShipmentItem():
    product: Product
    quantity: int

@dataclass
class Shipment():
    shipment_id: UUID
    items: List[ShipmentItem]
    shipment_datetime: datetime
