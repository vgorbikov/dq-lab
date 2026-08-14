from datetime import datetime, date, timedelta, timezone
import random
import os

import psycopg2
from dotenv import load_dotenv

from entities.common import Currency

from services.client_service import ClientService
from services.product_service import ProductService
from services.order_service import OrderService
from raw_data_translation import RawDataManager



random.seed(42)
START_TIME = datetime(2023, 1, 1, 0, 0, 1, 1, timezone(timedelta(hours=3)))
CLIENT_COUNT = 500
PRODUCT_COUNT = 900

def snaphot(dttm: datetime, cli: ClientService, prod: ProductService, ord: OrderService, dm: RawDataManager):
    for client in cli.clients:
        if client.is_having_updates:
            dm.write_client(client, load_dttm=dttm)
    for product in prod.products:
        if product.is_having_updates:
            dm.write_product(product, load_dttm=dttm)
    for stock in prod.stocks:
        if stock.is_having_updates:
            dm.write_stock(stock, load_dttm=dttm)
    for supply in prod.supplies:
        if supply.is_having_updates:
            dm.write_supply(supply, load_dttm=dttm)
    for shipment in prod.shipments:
        if shipment.is_having_updates:
            dm.write_shipment(shipment, load_dttm=dttm)
    for point in ord.pick_up_points:
        if point.is_having_updates:
            dm.write_pick_up_point(point, load_dttm=dttm)
    for order in ord.orders:
        if order.is_having_updates:
            dm.write_order(order, load_dttm=dttm)
    for cat in prod.categories:
        if cat.is_having_updates:
            dm.write_category(cat, load_dttm=dttm)

load_dotenv()

client_service = ClientService()
order_service = OrderService()
product_service = ProductService()

rwm = RawDataManager()

last_time = START_TIME


for cur in Currency.__members__.items():
    rwm.write_currency(cur[1], last_time)


for i in range(10000):
    last_time = last_time + timedelta(seconds=random.randint(1, 10000))

    if random.randint(1, 100) > 50:    # новый клиент
        print('>Новый клиент')
        client_service.new_client(registration_dttm=last_time, birthdate=last_time-timedelta(days=365*random.randint(12, 100)))

    if random.randint(1, 100) > 80:    # новый продукт
        print('>Новый продукт')
        product_service.new_product(creation_dttm=last_time)

    if random.randint(1, 100) > 95:     # новая точка выдачи
        print('>Новый пункт выдачи')
        order_service.new_pick_up_point(open_date=last_time)

    if random.randint(1, 100) > 30 \
        and len(client_service.clients) != 0 \
        and len(product_service.products) != 0 \
        and len(order_service.pick_up_points) != 0:   # новый заказ
        print('>Новый заказ')
        client = random.choice(client_service.clients)
        point = random.choice(order_service.pick_up_points)
        products = set([random.choice(product_service.products) for i in range(random.randint(1, 30))])
        positions = [(p, random.randint(1, 30)) for p in products]
        order_service.new_order(
            client=client,
            positions=positions,
            point=point,
            creation_dttm=last_time
        )

        product_service.new_shipment(   # и новая отгрузка
            dttm=last_time,
            items=positions
        )

    if random.randint(1, 100) > 50 and len(product_service.products) != 0:     # новая поставка
        print('>Новая поставка')
        products = set([random.choice(product_service.products) for i in range(random.randint(1, 100))])
        product_service.new_supply(
            dttm=last_time,
            items=[(p, random.randint(10, 1000)) for p in products]
        )

    if random.randint(1, 100) > 90 and len(product_service.products) != 0: # новая внеплановая отгрузка
        print('>Новая отгрузка')
        stocks = set([random.choice(product_service.stocks) for i in range(random.randint(1, 100))])
        products = [s.product for s in stocks if s.quantity > 100]
        product_service.new_shipment(
            dttm=last_time,
            items=[(p, random.randint(10, 50)) for p in products]
        )

    snaphot(last_time, client_service, product_service, order_service, rwm)
    print('snaphot')
