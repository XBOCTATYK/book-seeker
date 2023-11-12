from abc import ABC
from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import Session

from common.model.db.DictionaryDto import DictionaryDto
from datasource.DbLikeDataSource import DbLikeDataSource


class DbDictionary(ABC):
    _data_source: DbLikeDataSource
    _dict_items: dict

    def __init__(self, data_source: DbLikeDataSource, entity: Type[DictionaryDto]):
        self._data_source = data_source
        session: Session = self._data_source.open_session()
        db_result = session.execute(select(entity)).scalars().all()

        self._dict_items = {}

        for key in db_result:
            self._dict_items.setdefault(key.name, key.id)

        session.close()

    def select_by_id(self, type_name: str) -> int:
        return self._dict_items[type_name]

    def values(self):
        return list(map(lambda x: x, self._dict_items))
