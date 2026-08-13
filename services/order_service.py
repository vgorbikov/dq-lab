from uuid import uuid4, UUID
from typing import List, Dict, Tuple
import random
from datetime import datetime, date
from itertools import product

from entities.client_service import Client
from entities.product_service import Product
from entities.order_service import Order, OrderClient, OrderPosition, OrderProduct, OrderStatus, PickUpPoint
from common_generators import transliteration, AddressGenerator, generate_date



class OrderService():
    def __init__(self):
        self.address_gen: AddressGenerator = AddressGenerator()
        self.pick_up_points: List[PickUpPoint] = []
        self.orders: List[Order] = []
        self.clients: List[OrderClient] = []
        self.products: List[OrderProduct] = []
        

    def new_pick_up_point(self, open_date: date = generate_date(False)) -> PickUpPoint:
        point = PickUpPoint(
            point_id=uuid4(),
            address=self.address_gen.get_address(),
            open_date=open_date
        )

        self.pick_up_points.append(point)

        return point
    

    def new_order(self, client: Client, positions: List[Tuple[Product, int]], point: PickUpPoint = new_pick_up_point(), creation_dttm: datetime = datetime.now()) -> Order:
        if client.client_id in [c.client_id for c in self.clients]:
            order_client = [c for c in self.clients if c.client_id == client.client_id][0]
        else:
            order_client = OrderClient(
                    client_id=client.client_id,     # оставляем ID исходного клиента
                    name=client.name,
                    birthdate=client.birthdate,
                    phone_number=client.phone_number,
                    email=client.email
                )
            self.clients.append(OrderClient)
        order_positions = []
        for position in positions:
            pos_product = position[0]
            product = OrderProduct(
                product_id=uuid4(),                 # намеренно генерируем новый ID для того же продукта
                product_name=pos_product.product_name,
                weight_kg=pos_product.weight_kg,
                size=pos_product.size,
                sku=pos_product.sku,
                price=pos_product.price
            )
            self.products.append(product)
            order_positions.append(OrderPosition(product=product, quantity=position[1]))
        order = Order(
            order_id=uuid4(),
            positions=order_positions,
            client=order_client,
            status=OrderStatus.CREATED,
            pick_up_point=point,
            total_price=product.price,
            track_number=f'{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
            creation_dttm=creation_dttm,
            update_dttm=creation_dttm
        )
        self.orders.append(order)
        return order

    def change_order_status(self, order_id: UUID, status: OrderStatus, dttm: datetime = datetime.now()) -> Order:
        order = [o for o in self.orders if o.order_id == order_id][0]
        order.status = status
        order.update_dttm = dttm
        return order
