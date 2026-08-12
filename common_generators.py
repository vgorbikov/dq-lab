import random
from datetime import date, timedelta, datetime
from typing import List, Dict

from entities.common import Address



def transliteration(s: str) -> str:
    tt = str.maketrans('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя', 'ABVGDEEZZIIKLMNOPRSTUFHCCSS_I_EYYabvgdeezziiklmnoprstufhccss_i_eyy')
    return s.translate(tt)



def generate_date(adult_now: bool = True) -> date:
    if adult_now:
        max_date = datetime.now().date() - timedelta(365*18)
        min_date = date(1940, 1, 1)
    else:
        max_date= date(2026, 7, 30)
        min_date = datetime.now().date() - timedelta(365*18)
    days = max_date - min_date
    delta = random.randint(0, days.days)
    return min_date + timedelta(delta)



def create_email(firstname: str, lastname: str, valid: bool = random.choice([True, False])) -> str:
    return f'{transliteration(firstname[0])}{transliteration(lastname)}{random.randint(11, 99)}' + random.choice((
        '@yandex.ru' if valid else '2yandex.ru',
        '@mail.ru' if valid else '@mail.ry',
        '@ya.ru' if valid else 'ya,ru',
        '@inbox.ru' if valid else '@inbox>ru'
    ))



class FIOGenerator():
    def __init__(self):
        with open('./data_samples/f_i_o_samples.txt', 'r', encoding='utf-8') as f:
            data = f.readlines()
        self.fio_samples = data
        with open('./data_samples/f_i_samples.txt', 'r', encoding='utf-8') as f:
            data = f.readlines()
        self.io_samples = data


    def get_fio(self, is_full: bool = random.choice([True, False])):
        if is_full:
            return random.choice(self.fio_samples).strip()
        return random.choice(self.io_samples).strip()



class PhoneGenerator():
    '''
    Генератор случайных телефонных номеров
    '''
    def __init__(self):
        with open('./data_samples/phone_triplets.txt', 'r', encoding='utf-8') as f:
            data = f.readlines()
        self.data = data

    def get_phone(self, valid: bool = True):
        return ('+7' if valid else '7') + f'{self.data[random.randint(0, len(self.data)-1)].strip()}'+ \
        str(random.randint(0, 999)).zfill(3)+\
        str(random.randint(0, 99)).zfill(2)+\
        str(random.randint(0, 99)).zfill(2)



class AddressGenerator():
    def __init__(self):
        self.region_cities = self.__get_region_city_samples()
        self.streets = self.__get_street_samples()

    @staticmethod
    def __get_region_city_samples() -> Dict[str, List[str]]:
        with open('./data_samples/region_city_samples.txt', 'r', encoding='utf-8') as f:
            data = f.readlines()
        reg_cities = {}
        last_region = ''
        for line in data:
            if not line.startswith('    '):
                last_region = line.strip()
                reg_cities[last_region] = []
            else:
                reg_cities[last_region].append(line.strip())
        return reg_cities

    @staticmethod
    def __get_street_samples() -> List[str]:
        with open('./data_samples/street_samples.txt', 'r', encoding='utf-8') as f:
            data = f.readlines()
        return [s.strip() for s in data]

    def get_address(self) -> Address:
        region = random.choice([key for key in self.region_cities.keys()])
        city_prefix = random.choice(['', 'г. ', 'город '])
        street_prefix = random.choice(['', 'ул. ', 'улица '])
        house_prefix = random.choice(['', 'д. ', 'дом '])
        return Address(
            country='Россия',
            region=region,
            city=city_prefix + random.choice(self.region_cities[region]),
            street=street_prefix + random.choice(self.streets),
            house=house_prefix + str(random.randint(1, 200)),
            postal_code=str(random.randint(100000, 999999))
        )
