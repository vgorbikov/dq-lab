from typing import Any, List, Tuple
from dataclasses import dataclass
from datetime import date, datetime
from uuid import uuid4

import common_generators as dg

class Table():

    def to_insert(self) -> Tuple[Any]:
        attrs = self.__dict__
        keys = [i[0] for i in attrs.items()]
        keys.sort()
        return tuple([attrs[k] for k in keys])


    @classmethod
    def generate_ddl(cls, tablename: str, entities: List["Table"]):
        annotations = cls.__annotations__
        keys = [i[0] for i in annotations.items()]
        keys.sort()
        annotations = tuple([k for k in keys])
        delimiter = ',\n\t'
        return f"INSERT INTO {tablename} {annotations}"+\
        f"\nVALUES \n\t{delimiter.join([str(e.to_insert()) for e in entities])};"


@dataclass
class Client(Table):
    client_id: str              #PK
    fio: str                    #"ФИО клиента"
    birthdate: date             #"Дата рождения"
    status: str                 #"Статус клиента"
    phone: str                  #"Номер телефона клиента"
    email: str                  #"Электронная почта клиента"
    region: str                 #"Регион проживания клиента"
    deletion_flag: bool         #"Флаг удаления"
    version: int                #"Версия записи"
    effective_dttm: datetime    #"Временная метка начала действия записи"
