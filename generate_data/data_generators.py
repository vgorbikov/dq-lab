import random
from datetime import date, timedelta, datetime



def get_city(valid: bool = True):
    with open('./data_samples/city_samples.txt', 'r', encoding='utf-8') as f:
        data = f.readlines()
    return ('г. ' if valid else '') + data[random.randint(0, len(data)-1)].strip()



def transliteration(s: str) -> str:
    tt = str.maketrans('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя', 'ABVGDEEZZIIKLMNOPRSTUFHCCSS_I_EYYabvgdeezziiklmnoprstufhccss_i_eyy')
    return s.translate(tt)



def get_fio(valid: bool = True):
    if valid:
        with open('./data_samples/f_i_o_samples.txt', 'r', encoding='utf-8') as f:
            data = f.readlines()
    else:
        with open('./data_samples/f_i_samples.txt', 'r', encoding='utf-8') as f:
                    data = f.readlines()
    return data[random.randint(0, len(data)-1)].strip()



def get_phone(valid: bool = True):
    with open('./data_samples/phone_triplets.txt', 'r', encoding='utf-8') as f:
        data = f.readlines()
    return ('+7' if valid else '7') + f'{data[random.randint(0, len(data)-1)].strip()}'+ \
    str(random.randint(0, 999)).zfill(3)+\
    str(random.randint(0, 99)).zfill(2)+\
    str(random.randint(0, 99)).zfill(2)



def get_email(firstname: str, lastname: str, valid: bool = True) -> str:
    return f'{transliteration(firstname[0])}{transliteration(lastname)}' + random.choice((
        '@yandex.ru' if valid else '2yandex.ru',
        '@mail.ru' if valid else '@mail.ry',
        '@ya.ru' if valid else 'ya,ru',
        '@inbox.ru' if valid else '@inbox>ru'
    ))

def get_snils(valid: bool = True):
    nums = [random.randint(0, 9) for i in range(9)]
    chsum = str(sum([nums[i]*(9-i) for i in range(9)])%101)[-2:].zfill(2)
    nums = [str(n) for n in nums]
    return f"{''.join(nums[:3])}-{''.join(nums[3:6])}-{''.join(nums[6:9])} {chsum}" if valid \
    else f"{''.join(nums[:3])}{''.join(nums[3:6])}{''.join(nums[6:9])}{chsum}"


def get_date(adult_now: bool = True) -> date:
    if adult_now:
        max_date = datetime.now().date() - timedelta(365*18)
        min_date = date(1940, 1, 1)
    else:
        max_date= date(2026, 7, 30)
        min_date = datetime.now().date() - timedelta(365*18)
    days = max_date - min_date
    delta = random.randint(0, days.days)
    return min_date + timedelta(delta)
