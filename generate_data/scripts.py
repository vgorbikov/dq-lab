from datetime import datetime, date
from uuid import uuid4
import data_generators as dg

from tables import Client



def generate_valid():
    fio = dg.get_fio()
    sfio = fio.split(' ')
    return Client(
        client_id=uuid4(),
        fio=fio,
        birthdate=dg.get_date().isoformat(),
        status='Active',
        phone=dg.get_phone(),
        email=dg.get_email(sfio[1], sfio[0]),
        region=dg.get_city(),
        deletion_flag=False,
        version=1,
        effective_dttm=datetime.now()
    )

print(generate_valid())