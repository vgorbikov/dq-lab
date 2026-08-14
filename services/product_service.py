from uuid import uuid4
from typing import List, Dict, Tuple
import random
from datetime import datetime
from itertools import product

from entities.client_service import Client, Gender, Address
from entities.product_service import Product, ProductSize, ProductCategory, Shipment, ShipmentItem, Supply, SupplyItem, Stock
from entities.common import Price, Currency
from common_generators import transliteration



class ProductService():
    def __init__(self):
        self.sku_samples: List[Tuple[str, str]] = []
        self.cat_camples = self.__get_categoty_samples()

        for s in self.__get_product_samples():
            sku = transliteration(''.join([l[0] for l in s.split(' ')]).upper()) + str(random.randint(100, 999))
            self.sku_samples.append((sku, s))

        self.products: List[Product] = []
        self.categories: List[ProductCategory] = []
        self.cat_templates: Dict[str, ProductCategory] = {}
        self.stocks: List[Stock] = []
        self.supplies: List[Supply] = []
        self.shipments: List[Shipment] = []

        self._generate_categories()


    @staticmethod
    def __get_product_samples() -> List[str]:
        raw_samples = []
        with open('./data_samples/product_name_samples.txt', 'r', encoding='utf-8') as f:
            data = f.readlines()
        for line in data:
            raw_samples.append(line.strip().split(', '))

        samples = raw_samples[0]

        for level in raw_samples[1:]:
            samples = [' '.join(s) for s in list(product(samples, level))]

        return samples


    @staticmethod
    def __get_categoty_samples() -> Dict[str, Tuple[str, Tuple[str]]]:
        with open('./data_samples/product_category_samples.txt', 'r', encoding='utf-8') as f:
            data = f.readlines()
        samples = {}
        last_cat = ''
        for line in data:
            if not line.startswith('    '):
                last_cat, cat_description = line.strip().split(' - ')
                samples[last_cat] = (cat_description, [])
                continue
            samples[last_cat][1].append(line.strip())

        return samples
    

    def _generate_categories(self) -> None:
        '''
        Генерирует категории из текстового файла
        '''
        for sample_no in range(len(self.cat_camples)):
            sample = [i for i in self.cat_camples.items()][sample_no]
            cat = ProductCategory(
                category_id=sample_no,
                category_name=sample[0],
                description=sample[1][0],
                products=[]
            )

            self.categories.append(cat)
            for t in sample[1][1]:
                self.cat_templates[t] = cat


    def new_product(self, add_description: bool = random.choice([True, False]), creation_dttm: datetime = datetime.now()) -> Product:
        '''
        Создаёт новый продукт
        '''
        sku_sample = random.choice(self.sku_samples)
        category = [c[1] for c in self.cat_templates.items() if c[0] in sku_sample[1].split(' ')][0]
        product = Product(
            product_id=uuid4(),
            product_name=sku_sample[1],
            description=sku_sample[1] if add_description else None,
            category=category,
            weight_kg=0.01*random.randint(5, 100),
            sku=sku_sample[0],
            size=ProductSize(
                length=random.randint(1, 10),
                width=random.randint(1, 10),
                height=random.randint(1, 10)
            ),
            price=Price(
                amount_value=random.randint(100, 10000),
                currency=Currency.RUB
            )
        )

        category.products.append(product)

        stock = Stock(product=product, quantity=0, last_update=creation_dttm)
        self.stocks.append(stock)
        self.products.append(product)

        return product

    def new_supply(self, dttm: datetime = datetime.now(), items: List[Tuple[Product, int]] = None) -> Supply:
        if items is None:
            items = [(random.choice(self.products), random.randint(1, 10))]

        s_items = []

        for item in items:
            s_item = SupplyItem(
                product=item[0],
                quantity=item[1],
                batch_number=f'{random.randint(100000, 999999)} {random.randint(10, 99)}'
            )
            s_items.append(s_item)
            stock = [s for s in self.stocks if s.product.product_id == s_item.product.product_id][0]
            stock.quantity += item[1]

        supply = Supply(
            supply_id=uuid4(),
            supply_datetime=dttm,
            items=s_items
        )

        self.supplies.append(supply)

        return supply

    def new_shipment(self, dttm: datetime = datetime.now(), items: List[Tuple[Product, int]] = None) -> Shipment:
        if items is None:
            items = [(random.choice(self.products), random.randint(1, 10))]

        s_items = []

        for item in items:
            s_item = ShipmentItem(
                product=item[0],
                quantity=item[1]
            )
            s_items.append(s_item)
            stock = [s for s in self.stocks if s.product.product_id == s_item.product.product_id][0]
            stock.quantity -= item[1]

        shipment = Shipment(
            shipment_id=uuid4(),
            items=s_items,
            shipment_datetime=dttm
        )

        self.shipments.append(shipment)

        return shipment



