from datetime import datetime
from typing import Union, Callable, Dict, Any, Tuple
import os

import psycopg2

from entities.order_service import Order, OrderPosition, OrderProduct, OrderClient, PickUpPoint
from entities.client_service import Client
from entities.product_service import Product, ProductCategory, Shipment, Supply, SupplyItem, ShipmentItem, Stock
from entities.common import Currency



class RawDataManager():
    def __init__(self):
        self.conn = self.__get_db_connection()
        self.cur = self.conn.cursor()

    def __get_db_connection(self):
        return psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def __write_data(self, table: str, data: Dict) -> None:
        columns = list(data.keys())
        columns_str = ', '.join(columns)
        placeholders = ', '.join([f'%({c})s' for c in columns])

        query = f"""
        INSERT INTO {table} (
            {columns_str}
        ) VALUES (
            {placeholders}
        )
        ON CONFLICT DO NOTHING
        """

        self.cur.execute(query, data)
        self.conn.commit()


    def write_client(self, client: Union[Client, OrderClient], load_dttm: datetime):
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

        self.__write_data('raw.raw_client', data)
        client.be_writed()


    def write_product(self, product: Union[Product, OrderProduct], load_dttm: datetime):
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
                'price_currency': product.price.currency.name,
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
                'price_currency': product.price.currency.name,
                'src_system': 'order_service',
                'load_dttm': load_dttm
            }
        self.__write_data('raw.raw_product', data)
        product.be_writed()


    def write_category(self, categoty: ProductCategory, load_dttm: datetime):
        data = {
            'category_id': categoty.category_id,
            'category_name': categoty.category_name,
            'description': categoty.description,
            'src_system': 'product_service',
            'load_dttm': load_dttm
        }

        self.__write_data('raw.raw_category', data)
        categoty.be_writed()


    def write_currency(self, currency: Currency, load_dttm: datetime):
        data = {
            'currency_code': currency.name,
            'currency_name': currency.value,
            'src_system': 'common',
            'load_dttm': load_dttm
        }

        self.__write_data('raw.raw_currency', data)


    def write_stock(self, stock: Stock, load_dttm: datetime):
        data = {
            'product_id': stock.product.product_id.hex,
            'last_update': stock.last_update,
            'quantity': stock.quantity,
            'src_system': 'product_service',
            'load_dttm': load_dttm
        }

        self.__write_data('raw.raw_stock', data)
        stock.be_writed()


    def write_supply(self, supply: Supply, load_dttm: datetime):
        data = {
            'supply_id': supply.supply_id.hex,
            'supply_datetime': supply.supply_datetime,
            'src_system': 'product_service',
            'load_dttm': load_dttm
        }

        self.__write_data('raw.raw_supply', data)
        supply.be_writed()

        for position in supply.items:
            if not position.is_having_updates:
                continue
            pos_data = {
                'supply_id': supply.supply_id.hex,
                'product_id': position.product.product_id.hex,
                'quantity': position.quantity,
                'batch_number': position.batch_number,
                'src_system': 'product_service',
                'load_dttm': load_dttm
            }

            self.__write_data('raw.raw_supply_item', pos_data)
            position.be_writed()
        

    def write_shipment(self, shipment: Shipment, load_dttm: datetime):
        data = {
            'shipment_id': shipment.shipment_id.hex,
            'shipment_datetime': shipment.shipment_datetime,
            'src_system': 'product_service',
            'load_dttm': load_dttm
        }

        self.__write_data('raw.raw_shipment', data)
        shipment.be_writed()

        for position in shipment.items:
            if not position.is_having_updates:
                continue
            pos_data = {
                'shipment_id': shipment.shipment_id.hex,
                'product_id': position.product.product_id.hex,
                'quantity': position.quantity,
                'src_system': 'product_service',
                'load_dttm': load_dttm
            }

            self.__write_data('raw.raw_shipment_item', pos_data)
            position.be_writed()


    def write_order(self, order: Order, load_dttm: datetime):
        data = {
            'order_id': order.order_id.hex,
            'client_id': order.client.client_id.hex,
            'pick_up_point_id': order.pick_up_point.point_id.hex,
            'status': order.status.value,
            'track_number': order.track_number,
            'total_price_value': order.total_price.amount_value,
            'total_price_currency': order.total_price.currency.name,
            'creation_dttm': order.creation_dttm,
            'update_dttm': order.update_dttm,
            'src_system': 'order_service',
            'load_dttm': load_dttm
        }

        self.__write_data('raw.raw_order', data)
        order.be_writed()

        for position in order.positions:
            if not position.is_having_updates:
                continue
            pos_data = {
                'order_id': order.order_id.hex,
                'product_id': position.product.product_id.hex,
                'quantity': position.quantity,
                'src_system': 'order_service',
                'load_dttm': load_dttm
            }

            self.__write_data('raw.raw_order_position', pos_data)
            position.be_writed()


    def write_pick_up_point(self, point: PickUpPoint, load_dttm: datetime):
        data = {
            'point_id': point.point_id.hex,
            'open_date': point.open_date,
            'address_country': point.address.country,
            'address_region': point.address.region,
            'address_city': point.address.city,
            'address_street': point.address.street,
            'address_house': point.address.house,
            'address_postal_code': point.address.postal_code,
            'src_system': 'order_service',
            'load_dttm': load_dttm
        }

        self.__write_data('raw.raw_pick_up_point', data)
        point.be_writed()
