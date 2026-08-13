from datetime import datetime

import psycopg2

from services.client_service import ClientService
from write_raw_data import RawDataManager

cs = ClientService()
cl = cs.new_client()

print(cs.clients)

dm = RawDataManager()

dm.write_client(client=cl, load_dttm=datetime.now())

