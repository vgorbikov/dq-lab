from datetime import datetime
from typing import Union, Callable, Dict, Any, Tuple

import psycopg2

from entities.order_service import Order, OrderPosition, OrderProduct, OrderClient
from entities.client_service import Client
from entities.product_service import Product, ProductCategory, Shipment, Supply, SupplyItem, ShipmentItem, Stock
from entities.common import Currency



class RawDataManager():
    def __init__(self):
        self.conn = self.__get_db_connection()
        self.cur = self.conn.cursor()

    def __get_db_connection(self):
        return psycopg2.connect(
            host='localhost',
            port='5432',
            database='dq-practice',
            user='',
            password=''
        )

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def write_client(self, client: Union[Client, OrderClient], load_dttm: datetime):
        query = """
        INSERT INTO raw.raw_client (
            client_id, name, birthdate, gender, phone_number, email,
            registration_dttm, address_country, address_region, address_city,
            address_street, address_house, address_postal_code,
            src_system, load_dttm
        ) VALUES (
            %(client_id)s, %(name)s, %(birthdate)s, %(gender)s,
            %(phone_number)s, %(email)s, %(registration_dttm)s,
            %(address_country)s, %(address_region)s, %(address_city)s,
            %(address_street)s, %(address_house)s, %(address_postal_code)s,
            %(src_system)s, %(load_dttm)s
        )
        ON CONFLICT DO NOTHING
        """

        if isinstance(client, Client):
            data = {
                'client_id': client.client_id.hex,
                'name': client.name,
                'birthdate': client.birthdate,
                'gender': client.gender.value,
                'phone_number': client.phone_number,
                'email': client.email,
                'registration_dttm': client.registration_dttm,
                'address_country': client.residence_address.country,
                'address_region': client.residence_address.region,
                'address_city': client.residence_address.city,
                'address_street': client.residence_address.street,
                'address_house': client.residence_address.house,
                'address_postal_code': client.residence_address.postal_code,
                'src_system': 'client_service',
                'load_dttm': load_dttm
            } 
        if isinstance(client, OrderClient):
            data = {
                'client_id': client.client_id.hex,
                'name': client.name,
                'birthdate': client.birthdate,
                'gender': None,
                'phone_number': client.phone_number,
                'email': client.email,
                'registration_dttm': None,
                'address_country': None,
                'address_region': None,
                'address_city': None,
                'address_street': None,
                'address_house': None,
                'address_postal_code': None,
                'src_system': 'order_service',
                'load_dttm': load_dttm
            } 

        self.cur.execute(query, data)
        self.conn.commit()

    def write_product(self, product: Union[Product, OrderProduct], load_dttm: datetime):
        query = """
        INSERT INTO raw.raw_product (
            product_id, product_name, description, category_id, weight_kg,
            product_length, product_width, product_height, sku, price_value, 
            price_currency, src_system, load_dttm
        ) VALUES (
            %(product_id)s, %(product_name)s, %(description)s, %(category_id)s, %(weight_kg)s,
            %(product_length)s, %(product_width)s, %(product_height)s, %(sku)s, %(price_value)s, 
            %(price_currency)s, %(src_system)s, %(load_dttm)s
        )
        ON CONFLICT DO NOTHING
            """
        if isinstance(product, Product):
            data = {
                'product_id': product.product_id.hex,
                'product_name': product.product_name,
                'description': product.description,
                'category_id': product.category.category_id,
                'weight_kg': product.weight_kg,
                'product_length': product.size.length,
                'product_width': product.size.width,
                'product_height': product.size.height,
                'sku': product.sku,
                'price_value': product.price.amount_value,
                'price_currency': product.price.currency,
                'src_system': 'product_service',
                'load_dttm': load_dttm
            }
        if isinstance(product, OrderProduct):
            data = {
                'product_id': product.product_id.hex,
                'product_name': product.product_name,
                'description': None,
                'category_id': None,
                'weight_kg': product.weight_kg,
                'product_length': product.size.length,
                'product_width': product.size.width,
                'product_height': product.size.height,
                'sku': product.sku,
                'price_value': product.price.amount_value,
                'price_currency': product.price.currency,
                'src_system': 'order_service',
                'load_dttm': load_dttm
            }
        self.cur.execute(query, data)
        self.conn.commit()

# def write_raw_category(categoty: ProductCategory, load_dttm: datetime):
#     return {
#         'category_id': categoty.category_id,
#         'category_name': categoty.category_name,
#         'description': categoty.description,
#         'src_system': 'product_service',
#         'load_dttm': load_dttm
#     }

# def write_raw_currency(currency: Currency, load_dttm: datetime):
#     return {
#         'currency_id': 1,
#         'currency_code': currency.name,
#         'currency_name': currency.value,
#         'src_system': 'common',
#         'load_dttm': load_dttm
#     }

# def write_raw_stock(stock: Stock, load_dttm: datetime):
#     return {
#         'product_id': stock.product.product_id.hex,
#         'last_update': stock.last_update,
#         'quantity': stock.quantity,
#         'src_system': 'product_service',
#         'load_dttm': load_dttm
#     }

# def write_raw_supply(supply: Supply, load_dttm: datetime):
#     return {
#         'supply_id': supply.supply_id.hex,
#         'supply_datetime': supply.supply_datetime,
#         'src_system': 'product_service',
#         'load_dttm': load_dttm
#     }

# def write_raw_supply_item(item: SupplyItem, load_dttm: datetime):
#     return {
#         'supply_id': 1,
#         'product_id': item.product.product_id.hex,
#         'quantity':item.quantity,
#         'batch_number': item.batch_number,
#         'src_system': 'product_service',
#         'load_dttm': load_dttm
#     }

# def write_raw_order(order: Order):
#     return {

#     }
