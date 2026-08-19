from uuid import uuid4
from typing import List, Dict, Tuple
import random
from datetime import datetime
from itertools import product

from entities.client_service import Client, Gender, Address
from common_generators import PhoneGenerator, FIOGenerator, create_email, generate_date, AddressGenerator, transliteration



class ClientService():
    def __init__(self):
        self.clients: List[Client] = []
        self.fio_gen = FIOGenerator()
        self.address_gen = AddressGenerator()
        self.phone_gen = PhoneGenerator()


    def new_client(self, full_fio_flg: bool = random.choice([True, False]), birthdate: datetime = generate_date(), registration_dttm: datetime = generate_date()) -> Client:
        phone = self.phone_gen.get_phone()
        while phone in [c.phone_number for c in self.clients]:
            phone = self.phone_gen.get_phone()

        fio = self.fio_gen.get_fio(is_full=full_fio_flg)
        splitfio = fio.split(' ')
        email = create_email(firstname=splitfio[1], lastname=splitfio[0])

        client = Client(
            client_id=uuid4(),
            name=fio,
            birthdate=birthdate,
            gender=random.choice([Gender.MALE, Gender.FEMALE]),
            phone_number=phone,
            email=email if random.choice([True, False]) else None,
            residence_address=self.address_gen.get_address(),
            registration_dttm=registration_dttm
        )

        self.clients.append(client)

        return client
