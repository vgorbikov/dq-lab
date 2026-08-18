from datetime import datetime, date, timedelta, timezone
import random
import os

import psycopg2
from dotenv import load_dotenv

from entities.common import Currency, Price

from services.client_service import ClientService
from services.product_service import ProductService
from services.order_service import OrderService
from raw_data_translation import RawDataManager

from common_generators import PhoneGenerator



random.seed(42)
START_TIME = datetime(2023, 1, 1, 0, 0, 1, 1, timezone(timedelta(hours=3)))
ITER_COUNT = 3000

phone_gen = PhoneGenerator()

def snaphot(dttm: datetime, cli: ClientService, prod: ProductService, ord: OrderService, dm: RawDataManager):
    for client in cli.clients:
        if client.is_having_updates:
            dm.write_client(client, load_dttm=dttm)
    for client in ord.clients:
        if client.is_having_updates:
            dm.write_client(client, load_dttm=dttm)
    for product in prod.products:
        if product.is_having_updates:
            dm.write_product(product, load_dttm=dttm)
    for product in ord.products:
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



class Printer():
    def __init__(self):
        self.current_string = ''

    def print_over_last_string(self, string: str):
        print('\033[F\033[K'*self.current_string.count('\n'), end='')
        self.current_string = string 
        print(string, end='')

    def print_new_string(self, string: str):
        print('\b'*len(self.current_string))
        print(string)
        print(self.current_string)

printer = Printer()

load_dotenv()

client_service = ClientService()
order_service = OrderService()
product_service = ProductService()

rwm = RawDataManager()

last_time = START_TIME


for cur in Currency.__members__.items():
    rwm.write_currency(cur[1], last_time)


for i in range(ITER_COUNT):
    last_time = last_time + timedelta(seconds=random.randint(1, 50000))

    if random.randint(1, 100) > 50:    # новый клиент
        client_service.new_client(registration_dttm=last_time, birthdate=last_time-timedelta(days=365*random.randint(12, 100)))

    if random.randint(1, 100) > 75:    # новый продукт
        product_service.new_product(creation_dttm=last_time)

    if random.randint(1, 100) > 95:     # новая точка выдачи
        order_service.new_pick_up_point(open_date=last_time)

    if random.randint(1, 100) > 20 \
        and len(client_service.clients) != 0 \
        and len(product_service.products) != 0 \
        and len(order_service.pick_up_points) != 0:   # новый заказ

        client = random.choice(client_service.clients)
        point = random.choice(order_service.pick_up_points)
        products = list(set([random.choice(product_service.products) for i in range(random.randint(1, 10))]))
        stocks = [[s for s in product_service.stocks if p.product_id == s.product.product_id][0] for p in products]
        positions = [(products[i], random.randint(1, stocks[i].quantity)) for i in range(len(products)) if stocks[i].quantity > 0]
        if len(positions) != 0:
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

    if random.randint(1, 100) > 30 and len(product_service.products) != 0:     # новая поставка
        products = list(set([random.choice(product_service.products) for i in range(random.randint(1, 100))]))
        product_service.new_supply(
            dttm=last_time,
            items=[(p, random.randint(10, 1000)) for p in products]
        )

    if random.randint(1, 100) > 95 and len(product_service.products) != 0: # новая внеплановая отгрузка
        stocks = list(set([random.choice(product_service.stocks) for i in range(random.randint(1, 100))]))
        products = [s.product for s in stocks if s.quantity > 100]
        product_service.new_shipment(
            dttm=last_time,
            items=[(p, random.randint(10, 50)) for p in products]
        )

    if random.randint(1, 100) > 95 and len(client_service.clients) > 1:         # обновление телефона у клиента
        client = random.choice(client_service.clients)
        client.phone_number = phone_gen.get_phone()

    if random.randint(1, 100) > 70 and len(product_service.products) > 1:         # обновление цены по продукту
        product = random.choice(product_service.products)
        product.price = Price(
            amount_value=random.randint(200, 3000),
            currency=Currency.RUB
        )

    snaphot(last_time, client_service, product_service, order_service, rwm)
    info_string = f'Итерация {i}/{ITER_COUNT}; Время эмуляции: {last_time.isoformat(timespec="minutes", sep=" ")}'
    info_string += f'\n<client_service> Клиентов: {len(client_service.clients)}'
    info_string += f'\n<product_service> Продуктов: {len(product_service.products)}; ' 
    info_string += f'Отгрузок: {len(product_service.shipments)}; Поставок: {len(product_service.supplies)}'
    info_string += f'\n<order_service> Заказов: {len(order_service.orders)}; Пунктов выдачи: {len(order_service.pick_up_points)}; '
    info_string += f'Клиентов: {len(order_service.clients)}; Продуктов: {len(order_service.products)}'
    printer.print_over_last_string(info_string)
