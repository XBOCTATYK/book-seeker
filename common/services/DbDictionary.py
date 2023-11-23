from abc import ABC
from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import Session

from common.model.db.BaseDto import BaseDto
from datasource.DbLikeDataSource import DbLikeDataSource


class DbDictionary(ABC):
    _data_source: DbLikeDataSource
    _dict_items: dict[str, int]
    _dict_ids: dict[int, str] = {}

    def __init__(self, data_source: DbLikeDataSource, entity: Type[BaseDto]):
        self._data_source = data_source
        session: Session = self._data_source.open_session()
        db_result = session.execute(select(entity)).scalars().all()

        self._dict_items = {}

        for key in db_result:
            self._dict_items[key.name] = key.id
            self._dict_ids[key.id] = key.name

        session.close()

    def select_by_id(self, type_name: str) -> int:
        return self._dict_items[type_name]

    def select_name(self, item_id: int) -> str:
        return self._dict_ids[item_id]

    def get_dict(self) -> dict[str, int]:
        return self._dict_items

    def values(self) -> list[str]:
        return list(map(lambda x: x, self._dict_items))
