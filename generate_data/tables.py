from typing import Any, List, Tuple
from dataclasses import dataclass
from datetime import date, datetime
from uuid import uuid4

import data_generators as dg

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



@dataclass
class Document(Table):
    document_id: str            #PK
    client_id: str              #"Ссылка на клиента"
    series: str                 #"Серия документа"
    number: str                 #"Номер документа"
    document_type_code: int     #"Тип документа (ссылка на справочник)"
    issue_date:date             #"Дата выдачи документа"
    issued_by_department: str   #"Подразделение выдачи докуента"
    department_code: str        #"Код подразделения, выдавшего документ"
    residence: str              #"Место прописки"
    deletion_flag: bool         #"Флаг удаления"
    version: int                #"Версия записи"
    effective_dttm: datetime    #"Временная метка начала действия записи"


@dataclass
class DocumentType():
    document_type_id: int           #PK
    document_type_number: int       #"Числовой код документа"
    document_type_code: str         #"Буквенный код документа"
    document_type_description: str  #"Название документа"
    deletion_flag: bool             #"Флаг удаления"
    version: int                    #"Версия записи"
    effective_dttm: datetime        #"Временная метка начала действия записи"


@dataclass
class DebitCard():
    card_id: str                    #PK
    card_number: str                #"Номер карты"
    client_id: str                  #"Владелец карты"
    open_date: date                 #"Дата начала действия карты"
    expiration_date: date           #"Дата окончания действия карты" 
    deletion_flag: bool             #"Флаг удаления"
    version: int                    #"Версия записи"
    effective_dttm: datetime        #"Временная метка начала действия записи"
