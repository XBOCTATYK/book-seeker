from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.scavenger.models.db.FilterTypesTable import FilterTypesTable
from common.model.db.BaseDto import BaseDto
from datasource.DbLikeDataSource import DbLikeDataSource


class DbDictionary:
    _data_source: DbLikeDataSource
    _dict_items: dict

    def __init__(self, data_source: DbLikeDataSource, entity: Type[BaseDto]):
        self._data_source = data_source
        session: Session = self._data_source.open_session()
        db_result = session.execute(select(entity)).all()

        self._dict_items = {}

        for dict_item in db_result:
            key: FilterTypesTable = dict_item[0]
            self._dict_items.setdefault(key.name, key.id)

        session.close()

    def select_by_id(self, type_name: str) -> int:
        return self._dict_items[type_name]

    def values(self):
        return list(map(lambda x: x, self._dict_items))
