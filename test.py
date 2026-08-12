from uuid import uuid4
from typing import List, Dict, Tuple
import random
from datetime import datetime
from itertools import product

from entities.client_service import Client, Gender, Address
from entities.product_service import Product, ProductSize, ProductCategory
from common_generators import PhoneGenerator, FIOGenerator, create_email, generate_date, AddressGenerator, transliteration



class ClientService():
    def __init__(self):
        self.clients: List[Client] = []
        self.fio_gen = FIOGenerator()
        self.address_gen = AddressGenerator()
        self.phone_gen = PhoneGenerator()


    def new_client(self, full_fio_flg: bool = True, adult_flg: bool = True, registration_dttm: datetime = generate_date()) -> Client:
        phone = self.phone_gen.get_phone()
        while phone in [c.phone_number for c in self.clients]:
            phone = self.phone_gen.get_phone()

        fio = self.fio_gen.get_fio(is_full=full_fio_flg)
        splitfio = fio.split(' ')
        email = create_email(firstname=splitfio[1], lastname=splitfio[0])

        client = Client(
            client_id=uuid4(),
            name=fio,
            birthdate=generate_date(adult_now=adult_flg),
            gender=random.choice([Gender.MALE, Gender.FEMALE]),
            phone_number=phone,
            email=email,
            residence_address=self.address_gen.get_address(),
            registration_dttm=registration_dttm
        )

        self.clients.append(client)

        return client


class ProductService():
    def __init__(self):
        self.sku_samples: List[Tuple[str, str]] = []

        for s in self.__get_product_samples():
            sku = transliteration(''.join([l[0] for l in s.split(' ')]).upper()) + str(random.randint(100, 999))
            self.sku_samples.append(sku, s)

        self.products = []


    @staticmethod
    def __get_product_samples() -> List[str]:
        raw_samples = []
        with open('./generate_data/data_samples/product_name_samples.txt', 'r', encoding='utf-8') as f:
            data = f.readlines()
        for line in data:
            raw_samples.append(line.strip().split(', '))

        samples = raw_samples[0]

        for level in raw_samples[1:]:
            samples = [' '.join(s) for s in list(product(samples, level))]

        return samples

    def new_product(self) -> Product:
        sku_sample = random.choice(self.sku_samples)
        product = Product(
            product_id=uuid4(),
            product_name=sku_sample[1],
            description=sku_sample[1],
            category=ProductCategory(
                category_id=uuid4(),
                description=' ',
                products=[]
            ),
            weight_kg=0.01*random.randint(5, 100),
            sku=sku_sample[0],
            size=ProductSize(
                length=random.randint(1, 10),
                width=random.randint(1, 10),
                height=random.randint(1, 10)
            ),
            price=random.randint(100, 5000)
        )
